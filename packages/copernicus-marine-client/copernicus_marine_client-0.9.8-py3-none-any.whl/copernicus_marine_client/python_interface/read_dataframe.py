import pathlib
from datetime import datetime
from typing import List, Optional, Union

import pandas

from copernicus_marine_client.catalogue_parser.request_structure import (
    LoadRequest,
)
from copernicus_marine_client.core_functions.deprecated import (
    deprecated_python_option,
    log_deprecated_message,
)
from copernicus_marine_client.core_functions.deprecated_options import (
    DEPRECATED_OPTIONS,
)
from copernicus_marine_client.download_functions.download_arco_series import (
    read_dataframe_from_arco_series,
)
from copernicus_marine_client.download_functions.download_opendap import (
    read_dataframe_from_opendap,
)
from copernicus_marine_client.download_functions.subset_parameters import (
    DepthParameters,
    GeographicalParameters,
    LatitudeParameters,
    LongitudeParameters,
    TemporalParameters,
)
from copernicus_marine_client.python_interface.exception_handler import (
    log_exception_and_exit,
)
from copernicus_marine_client.python_interface.load_utils import (
    load_data_object_from_load_request,
)
from copernicus_marine_client.python_interface.utils import homogenize_datetime


@log_exception_and_exit
def load_pandas_dataframe(*args, **kwargs):
    """
    Deprecated function, use 'read_dataframe' instead.
    """
    log_deprecated_message("load_pandas_dataframe", "read_dataframe")
    return read_dataframe(*args, **kwargs)


@deprecated_python_option(**DEPRECATED_OPTIONS.dict_old_names_to_new_names)
@log_exception_and_exit
def read_dataframe(
    dataset_url: Optional[str] = None,
    dataset_id: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    variables: Optional[List[str]] = None,
    minimum_longitude: Optional[float] = None,
    maximum_longitude: Optional[float] = None,
    minimum_latitude: Optional[float] = None,
    maximum_latitude: Optional[float] = None,
    minimum_depth: Optional[float] = None,
    maximum_depth: Optional[float] = None,
    vertical_dimension_as_originally_produced: bool = True,
    start_datetime: Optional[Union[datetime, str]] = None,
    end_datetime: Optional[Union[datetime, str]] = None,
    force_service: Optional[str] = None,
    credentials_file: Optional[Union[pathlib.Path, str]] = None,
    overwrite_metadata_cache: bool = False,
    no_metadata_cache: bool = False,
) -> pandas.DataFrame:
    """
    Load a Pandas DataFrame containing Copernicus Marine data from a specified dataset.

    Args:
        dataset_url (str, optional): The URL of the dataset.
        dataset_id (str, optional): The identifier of the dataset.
        username (str, optional): Username for authentication.
        password (str, optional): Password for authentication.
        variables (List[str], optional): List of variable names to load.
        minimum_longitude (float, optional): Minimum longitude for spatial subset.
        maximum_longitude (float, optional): Maximum longitude for spatial subset.
        minimum_latitude (float, optional): Minimum latitude for spatial subset.
        maximum_latitude (float, optional): Maximum latitude for spatial subset.
        minimum_depth (float, optional): Minimum depth for vertical subset.
        maximum_depth (float, optional): Maximum depth for vertical subset.
        vertical_dimension_as_originally_produced (bool, optional): If True, use the vertical dimension as originally produced.
        start_datetime (datetime, optional): Start datetime for temporal subset.
        end_datetime (datetime, optional): End datetime for temporal subset.
        force_service (str, optional): Force a specific service for data download.
        credentials_file (Union[pathlib.Path, str], optional): Path to a credentials file for authentication.
        overwrite_metadata_cache (bool, optional): If True, overwrite the metadata cache.
        no_metadata_cache (bool, optional): If True, do not use metadata caching.

    Returns:
        pandas.DataFrame: A DataFrame containing the loaded Copernicus Marine data.
    """  # noqa
    start_datetime = homogenize_datetime(start_datetime)
    end_datetime = homogenize_datetime(end_datetime)
    credentials_file = (
        pathlib.Path(credentials_file) if credentials_file else None
    )
    load_request = LoadRequest(
        dataset_url=dataset_url,
        dataset_id=dataset_id,
        username=username,
        password=password,
        variables=variables,
        geographical_parameters=GeographicalParameters(
            latitude_parameters=LatitudeParameters(
                minimum_latitude=minimum_latitude,
                maximum_latitude=maximum_latitude,
            ),
            longitude_parameters=LongitudeParameters(
                minimum_longitude=minimum_longitude,
                maximum_longitude=maximum_longitude,
            ),
        ),
        temporal_parameters=TemporalParameters(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        ),
        depth_parameters=DepthParameters(
            minimum_depth=minimum_depth,
            maximum_depth=maximum_depth,
            vertical_dimension_as_originally_produced=vertical_dimension_as_originally_produced,  # noqa
        ),
        force_service=force_service,
        credentials_file=credentials_file,
        overwrite_metadata_cache=overwrite_metadata_cache,
        no_metadata_cache=no_metadata_cache,
    )
    dataset = load_data_object_from_load_request(
        load_request,
        read_dataframe_from_arco_series,
        read_dataframe_from_opendap,
    )
    return dataset
