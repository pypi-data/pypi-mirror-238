import logging
from datetime import datetime
from decimal import Decimal
from typing import List, Literal, Optional, Union

import numpy as np
import xarray

from copernicus_marine_client.download_functions.subset_parameters import (
    DepthParameters,
    GeographicalParameters,
    LatitudeParameters,
    LongitudeParameters,
    TemporalParameters,
)

logger = logging.getLogger("copernicus_marine_root_logger")

COORDINATES_LABEL = {
    "latitude": ["latitude", "nav_lat", "x", "lat"],
    "longitude": ["longitude", "nav_lon", "y", "lon"],
    "time": ["time_counter", "time"],
    "depth": ["depth", "deptht", "elevation"],
}


class MinimumLongitudeGreaterThanMaximumLongitude(Exception):
    pass


class VariableDoesNotExistInTheDataset(Exception):
    def __init__(self, variable):
        super().__init__()
        self.__setattr__(
            "custom_exception_message",
            f"The variable '{variable}' is neither a variable or a standard name in the dataset",  # noqa
        )


def _dataset_custom_sel(
    dataset: xarray.Dataset,
    coord_type: Literal["latitude", "longitude", "depth", "time"],
    coord_selection: Union[float, slice, datetime, None],
    method: Union[str, None] = None,
) -> xarray.Dataset:
    for coord_label in COORDINATES_LABEL[coord_type]:
        if coord_label in dataset.coords:
            dataset = dataset.sel(
                {coord_label: coord_selection}, method=method
            )
    return dataset


def _coordinates_custom_sel(
    coordinates: xarray.Coordinates,
    coord_type: Literal["latitude", "longitude", "depth", "time"],
    coord_selection: Union[float, slice, datetime, None],
    method: Union[str, None] = None,
) -> xarray.Coordinates:
    for coord_label in COORDINATES_LABEL[coord_type]:
        if coord_label in coordinates:
            coordinates = coordinates.assign(
                coordinates[coord_label]
                .sel({coord_label: coord_selection}, method=method)
                .coords
            )
    return coordinates


def _xarray_data_object_custom_sel(
    data_object: Union[xarray.Dataset, xarray.Coordinates],
    coord_type: Literal["latitude", "longitude", "depth", "time"],
    coord_selection: Union[float, slice, datetime, None],
    method: Union[str, None] = None,
) -> Union[xarray.Dataset, xarray.Coordinates]:
    if isinstance(data_object, xarray.Dataset):
        return _dataset_custom_sel(
            data_object, coord_type, coord_selection, method
        )
    if isinstance(data_object, xarray.Coordinates):
        return _coordinates_custom_sel(
            data_object, coord_type, coord_selection, method
        )
    return data_object


def _update_dataset_attributes(dataset: xarray.Dataset):
    for coord_label in COORDINATES_LABEL["longitude"]:
        if coord_label in dataset.coords:
            attrs = dataset[coord_label].attrs
            if "valid_min" in attrs:
                attrs["valid_min"] += 180
            if "valid_max" in attrs:
                attrs["valid_max"] += 180
            dataset = dataset.assign_coords(
                {coord_label: dataset[coord_label] % 360}
            ).sortby(coord_label)
            dataset[coord_label].attrs = attrs
    return dataset


def _update_coordinates_attributes(coordinates: xarray.Coordinates):
    for coord_label in COORDINATES_LABEL["longitude"]:
        if coord_label in coordinates:
            attrs = coordinates[coord_label].attrs
            if "valid_min" in attrs:
                attrs["valid_min"] += 180
            if "valid_max" in attrs:
                attrs["valid_max"] += 180
            coordinates = coordinates.assign(
                coordinates[coord_label]
                .assign_coords({coord_label: coordinates[coord_label] % 360})
                .sortby(coord_label)
                .coords
            )
            coordinates[coord_label].attrs = attrs
    return coordinates


def _update_data_object_attributes(
    data_object: Union[xarray.Dataset, xarray.Coordinates]
):
    if isinstance(data_object, xarray.Dataset):
        return _update_dataset_attributes(data_object)
    if isinstance(data_object, xarray.Coordinates):
        return _update_coordinates_attributes(data_object)
    return data_object


def _latitude_subset(
    data_object: Union[xarray.Dataset, xarray.Coordinates],
    latitude_parameters: LatitudeParameters,
) -> xarray.Dataset:
    minimum_latitude = latitude_parameters.minimum_latitude
    maximum_latitude = latitude_parameters.maximum_latitude
    if minimum_latitude is not None or maximum_latitude is not None:
        latitude_selection = (
            minimum_latitude
            if minimum_latitude == maximum_latitude
            else slice(minimum_latitude, maximum_latitude)
        )
        latitude_method = (
            "nearest" if minimum_latitude == maximum_latitude else None
        )
        data_object = _xarray_data_object_custom_sel(
            data_object, "latitude", latitude_selection, latitude_method
        )
    return data_object


def _longitude_subset(
    data_object: Union[xarray.Dataset, xarray.Coordinates],
    longitude_parameters: LongitudeParameters,
) -> xarray.Dataset:
    minimum_longitude = longitude_parameters.minimum_longitude
    maximum_longitude = longitude_parameters.maximum_longitude
    if minimum_longitude is not None or maximum_longitude is not None:
        if minimum_longitude is not None and maximum_longitude is not None:
            if minimum_longitude > maximum_longitude:
                raise MinimumLongitudeGreaterThanMaximumLongitude(
                    "--minimum-longitude option must be smaller "
                    "or equal to --maximum-longitude"
                )
            if maximum_longitude - minimum_longitude >= 360:
                longitude_selection: Union[float, slice, None] = None
            elif minimum_longitude == maximum_longitude:
                longitude_selection = longitude_modulus(minimum_longitude)
                longitude_method = "nearest"
            else:
                minimum_longitude_modulus = longitude_modulus(
                    minimum_longitude
                )
                maximum_longitude_modulus = longitude_modulus(
                    maximum_longitude
                )
                if maximum_longitude_modulus < minimum_longitude_modulus:
                    maximum_longitude_modulus += 360
                    data_object = _update_data_object_attributes(data_object)
                longitude_selection = slice(
                    minimum_longitude_modulus,
                    maximum_longitude_modulus,
                )
                longitude_method = None
        else:
            longitude_selection = slice(minimum_longitude, maximum_longitude)
            longitude_method = None

        if longitude_selection is not None:
            data_object = _xarray_data_object_custom_sel(
                data_object, "longitude", longitude_selection, longitude_method
            )
    return data_object


def _temporal_subset(
    data_object: Union[xarray.Dataset, xarray.Coordinates],
    temporal_parameters: TemporalParameters,
) -> xarray.Dataset:
    start_datetime = temporal_parameters.start_datetime
    end_datetime = temporal_parameters.end_datetime
    if start_datetime is not None or end_datetime is not None:
        temporal_selection = (
            start_datetime
            if start_datetime == end_datetime
            else slice(start_datetime, end_datetime)
        )
        temporal_method = "nearest" if start_datetime == end_datetime else None
        data_object = _xarray_data_object_custom_sel(
            data_object, "time", temporal_selection, temporal_method
        )
    return data_object


def _depth_subset(
    data_object: Union[xarray.Dataset, xarray.Coordinates],
    depth_parameters: DepthParameters,
) -> xarray.Dataset:
    def convert_elevation_to_depth(dataset: xarray.Dataset):
        if "elevation" in dataset.coords:
            attrs = dataset["elevation"].attrs
            dataset = dataset.reindex(elevation=dataset.elevation[::-1])
            dataset["elevation"] = dataset.elevation * (-1)
            dataset = dataset.rename({"elevation": "depth"})
            dataset.depth.attrs = attrs
        return dataset

    if (
        depth_parameters.vertical_dimension_as_originally_produced
        and isinstance(data_object, xarray.Dataset)
    ):
        data_object = convert_elevation_to_depth(data_object)
    minimum_depth = depth_parameters.minimum_depth
    maximum_depth = depth_parameters.maximum_depth
    if minimum_depth is not None or maximum_depth is not None:
        coords = (
            data_object.coords
            if isinstance(data_object, xarray.Dataset)
            else data_object
        )
        if "elevation" in coords:
            minimum_depth = (
                minimum_depth * -1.0 if minimum_depth is not None else None
            )
            maximum_depth = (
                maximum_depth * -1.0 if maximum_depth is not None else None
            )
            minimum_depth, maximum_depth = maximum_depth, minimum_depth

        depth_selection = (
            minimum_depth
            if minimum_depth == maximum_depth
            else slice(minimum_depth, maximum_depth)
        )
        depth_method = "nearest" if minimum_depth == maximum_depth else None
        data_object = _xarray_data_object_custom_sel(
            data_object, "depth", depth_selection, depth_method
        )
    return data_object


def _get_variable_name_from_standard_name(
    dataset: xarray.Dataset, standard_name: str
) -> Optional[str]:
    for variable_name in dataset.variables:
        if (
            hasattr(dataset[variable_name], "standard_name")
            and dataset[variable_name].standard_name == standard_name
        ):
            return str(variable_name)
    return None


def _variables_subset(
    dataset: xarray.Dataset, variables: List[str]
) -> xarray.Dataset:
    dataset_variables_filter = []

    for variable in variables:
        if variable in dataset.variables:
            dataset_variables_filter.append(variable)
        else:
            variable_name_from_standard_name = (
                _get_variable_name_from_standard_name(dataset, variable)
            )
            if variable_name_from_standard_name is not None:
                dataset_variables_filter.append(
                    variable_name_from_standard_name
                )
            else:
                raise VariableDoesNotExistInTheDataset(variable)
    return dataset[np.array(dataset_variables_filter)]


def subset(
    data_object: Union[xarray.Dataset, xarray.Coordinates],
    variables: Optional[List[str]],
    geographical_parameters: GeographicalParameters,
    temporal_parameters: TemporalParameters,
    depth_parameters: DepthParameters,
) -> xarray.Dataset:
    if variables and isinstance(data_object, xarray.Dataset):
        data_object = _variables_subset(data_object, variables)

    data_object = _latitude_subset(
        data_object, geographical_parameters.latitude_parameters
    )
    data_object = _longitude_subset(
        data_object, geographical_parameters.longitude_parameters
    )

    data_object = _temporal_subset(data_object, temporal_parameters)

    data_object = _depth_subset(data_object, depth_parameters)

    return data_object


def longitude_modulus(longitude: float) -> float:
    """
    Returns the equivalent longitude between -180 and 180
    """
    # We are using Decimal to avoid issue with rounding
    modulus = float(Decimal(str(longitude + 180)) % 360)
    # Modulus with python return a negative value if the denominator is negative
    # To counteract that, we add 360 if the result is < 0
    modulus = modulus if modulus >= 0 else modulus + 360
    return modulus - 180
