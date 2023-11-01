import json
import logging
import pathlib
import sys
from datetime import datetime
from typing import List, Optional

from copernicus_marine_client.catalogue_parser.catalogue_parser import (
    CopernicusMarineDatasetServiceType,
    get_dataset_and_suffix_path_from_url,
    parse_catalogue,
)
from copernicus_marine_client.catalogue_parser.request_structure import (
    SubsetRequest,
    convert_motu_api_request_to_structure,
    subset_request_from_file,
)
from copernicus_marine_client.core_functions.credentials_utils import (
    get_and_check_username_password,
)
from copernicus_marine_client.core_functions.services_utils import (
    CommandType,
    get_dataset_service_and_suffix_path,
)
from copernicus_marine_client.core_functions.utils import get_unique_filename
from copernicus_marine_client.download_functions.download_arco_series import (
    download_zarr,
)
from copernicus_marine_client.download_functions.download_motu import (
    download_motu,
)
from copernicus_marine_client.download_functions.download_opendap import (
    download_opendap,
)

logger = logging.getLogger("copernicus_marine_root_logger")


def subset_function(
    dataset_url: Optional[str],
    dataset_id: Optional[str],
    username: Optional[str],
    password: Optional[str],
    variables: Optional[List[str]],
    minimum_longitude: Optional[float],
    maximum_longitude: Optional[float],
    minimum_latitude: Optional[float],
    maximum_latitude: Optional[float],
    minimum_depth: Optional[float],
    maximum_depth: Optional[float],
    vertical_dimension_as_originally_produced: bool,
    start_datetime: Optional[datetime],
    end_datetime: Optional[datetime],
    output_filename: Optional[pathlib.Path],
    force_service: Optional[str],
    request_file: Optional[pathlib.Path],
    output_directory: Optional[pathlib.Path],
    credentials_file: Optional[pathlib.Path],
    motu_api_request: Optional[str],
    force_download: bool,
    overwrite_output_data: bool,
    overwrite_metadata_cache: bool,
    no_metadata_cache: bool,
    staging: bool,
) -> pathlib.Path:
    subset_request = SubsetRequest()
    if request_file:
        subset_request = subset_request_from_file(request_file)
    if motu_api_request:
        motu_api_subset_request = convert_motu_api_request_to_structure(
            motu_api_request
        )
        subset_request.update(motu_api_subset_request.__dict__)
    request_update_dict = {
        "dataset_url": dataset_url,
        "dataset_id": dataset_id,
        "variables": variables,
        "minimum_longitude": minimum_longitude,
        "maximum_longitude": maximum_longitude,
        "minimum_latitude": minimum_latitude,
        "maximum_latitude": maximum_latitude,
        "minimum_depth": minimum_depth,
        "maximum_depth": maximum_depth,
        "vertical_dimension_as_originally_produced": vertical_dimension_as_originally_produced,  # noqa
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "output_filename": output_filename,
        "force_service": force_service,
        "output_directory": output_directory,
    }
    subset_request.update(request_update_dict)
    username, password = get_and_check_username_password(
        username,
        password,
        credentials_file,
    )
    if all(
        e is None
        for e in [
            subset_request.variables,
            subset_request.minimum_longitude,
            subset_request.maximum_longitude,
            subset_request.minimum_latitude,
            subset_request.maximum_latitude,
            subset_request.minimum_depth,
            subset_request.maximum_depth,
            subset_request.start_datetime,
            subset_request.end_datetime,
        ]
    ):
        if not subset_request.dataset_id:
            if subset_request.dataset_url:
                catalogue = parse_catalogue(
                    overwrite_metadata_cache=overwrite_metadata_cache,
                    no_metadata_cache=no_metadata_cache,
                    staging=staging,
                )
                (dataset, _) = get_dataset_and_suffix_path_from_url(
                    catalogue, subset_request.dataset_url
                )
                dataset_id = dataset.dataset_id
            else:
                syntax_error = SyntaxError(
                    "Must specify at least one of "
                    "'dataset_url' or 'dataset_id' options"
                )
                raise syntax_error
        logger.error(
            "Missing subset option. Try 'copernicus-marine subset --help'."
        )
        logger.info(
            "To retrieve a complete dataset, please use instead: "
            f"copernicus-marine get --dataset-id {subset_request.dataset_id}"
        )
        sys.exit(1)
    # Specific treatment for default values:
    # In order to not overload arguments with default values
    if force_download:
        subset_request.force_download = force_download
    if overwrite_output_data:
        subset_request.overwrite_output_data = overwrite_output_data

    catalogue = parse_catalogue(
        overwrite_metadata_cache=overwrite_metadata_cache,
        no_metadata_cache=no_metadata_cache,
        staging=staging,
    )
    dataset_service, _ = get_dataset_service_and_suffix_path(
        catalogue,
        subset_request.dataset_id,
        subset_request.dataset_url,
        subset_request.force_service,
        CommandType.SUBSET,
        subset_request.get_time_and_geographical_subset(),
    )
    subset_request.dataset_url = dataset_service.uri
    logger.info(
        "Downloading using service "
        f"{dataset_service.service_type.service_name.value}..."
    )
    if dataset_service.service_type in [
        CopernicusMarineDatasetServiceType.GEOSERIES,
        CopernicusMarineDatasetServiceType.TIMESERIES,
    ]:
        output_path = download_zarr(
            username,
            password,
            subset_request,
        )
    elif (
        dataset_service.service_type
        == CopernicusMarineDatasetServiceType.OPENDAP
    ):
        output_path = download_opendap(
            username,
            password,
            subset_request,
        )
    elif (
        dataset_service.service_type == CopernicusMarineDatasetServiceType.MOTU
    ):
        output_path = download_motu(
            username,
            password,
            subset_request,
            catalogue=catalogue,
        )
    return output_path


def create_subset_template() -> None:
    filename = get_unique_filename(
        filepath=pathlib.Path("subset_template.json"), overwrite_option=False
    )
    with open(filename, "w") as output_file:
        json.dump(
            {
                "dataset_id": "cmems_mod_glo_phy_anfc_0.083deg_P1D-m",
                "start_datetime": "2023-10-07",
                "end_datetime": "2023-10-12",
                "minimum_longitude": -85,
                "maximum_longitude": -10,
                "minimum_latitude": 35,
                "maximum_latitude": 43,
                "minimum_depth": False,
                "maximum_depth": False,
                "variables": ["zos", "tob"],
                "output_directory": "copernicusmarine_data",
                "output_filename": (
                    "GLO12-lon85Wlon10W-lat35Nlat43N"
                    "--from20231007to20231012.nc"
                ),
                "force_service": False,
                "force_download": False,
                "request_file": False,
                "motu_api_request": False,
                "overwrite_output_data": False,
                "overwrite_metadata_cache": False,
                "no_metadata_cache": False,
            },
            output_file,
            indent=4,
        )
    logger.info(f"Template created at: {filename}")
