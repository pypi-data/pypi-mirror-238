import fnmatch
import json
import logging
import pathlib
from typing import List, Optional

from copernicus_marine_client.catalogue_parser.catalogue_parser import (
    CopernicusMarineDatasetServiceType,
    parse_catalogue,
)
from copernicus_marine_client.catalogue_parser.request_structure import (
    GetRequest,
    get_request_from_file,
)
from copernicus_marine_client.core_functions.credentials_utils import (
    get_and_check_username_password,
)
from copernicus_marine_client.core_functions.services_utils import (
    CommandType,
    get_dataset_service_and_suffix_path,
)
from copernicus_marine_client.core_functions.utils import get_unique_filename
from copernicus_marine_client.download_functions.download_ftp import (
    download_ftp,
)
from copernicus_marine_client.download_functions.download_original_files import (
    download_original_files,
)

logger = logging.getLogger("copernicus_marine_root_logger")


def get_function(
    dataset_url: Optional[str],
    dataset_id: Optional[str],
    username: Optional[str],
    password: Optional[str],
    no_directories: bool,
    show_outputnames: bool,
    output_directory: Optional[pathlib.Path],
    credentials_file: Optional[pathlib.Path],
    force_download: bool,
    overwrite_output_data: bool,
    request_file: Optional[pathlib.Path],
    force_service: Optional[str],
    overwrite_metadata_cache: bool,
    no_metadata_cache: bool,
    filter: Optional[str],
    regex: Optional[str],
    staging: bool,
) -> List[pathlib.Path]:
    get_request = GetRequest()
    if request_file:
        get_request = get_request_from_file(request_file)
    request_update_dict = {
        "dataset_url": dataset_url,
        "dataset_id": dataset_id,
        "output_directory": output_directory,
        "force_service": force_service,
    }
    get_request.update(request_update_dict)

    # Specific treatment for default values:
    # In order to not overload arguments with default values
    if no_directories:
        get_request.no_directories = no_directories
    if show_outputnames:
        get_request.show_outputnames = show_outputnames
    if force_download:
        get_request.force_download = force_download
    if overwrite_output_data:
        get_request.overwrite_output_data = overwrite_output_data
    if force_service:
        get_request.force_service = force_service
    if filter:
        get_request.regex = _filter_to_regex(filter)
    if regex:
        get_request.regex = _overload_regex_with_filter(regex, filter)

    return _run_get_request(
        username,
        password,
        get_request,
        credentials_file,
        overwrite_metadata_cache,
        no_metadata_cache,
        staging=staging,
    )


def _filter_to_regex(filter: str) -> str:
    return fnmatch.translate(filter)


def _overload_regex_with_filter(regex: str, filter: Optional[str]) -> str:
    return (
        "(" + regex + "|" + _filter_to_regex(filter) + ")" if filter else regex
    )


def _run_get_request(
    username: Optional[str],
    password: Optional[str],
    get_request: GetRequest,
    credentials_file: Optional[pathlib.Path],
    overwrite_metadata_cache: bool,
    no_metadata_cache: bool,
    staging: bool = False,
) -> List[pathlib.Path]:
    username, password = get_and_check_username_password(
        username,
        password,
        credentials_file,
    )
    catalogue = parse_catalogue(
        overwrite_metadata_cache=overwrite_metadata_cache,
        no_metadata_cache=no_metadata_cache,
        staging=staging,
    )
    dataset_service, suffix_path = get_dataset_service_and_suffix_path(
        catalogue,
        get_request.dataset_id,
        get_request.dataset_url,
        get_request.force_service,
        CommandType.GET,
    )
    get_request.dataset_url = dataset_service.uri
    if suffix_path:
        filter = f"*{suffix_path}*"
        logger.info("Using dataset URL suffix path as filter " f"{filter}")
        get_request.regex = (
            _overload_regex_with_filter(get_request.regex, filter)
            if get_request.regex
            else _filter_to_regex(filter)
        )
    logger.info(
        "Downloading using service "
        f"{dataset_service.service_type.service_name.value}..."
    )
    downloaded_files = (
        download_ftp(
            username,
            password,
            get_request,
        )
        if dataset_service.service_type
        == CopernicusMarineDatasetServiceType.FTP
        else download_original_files(
            username,
            password,
            get_request,
        )
    )
    logger.info(downloaded_files)
    return downloaded_files


def create_get_template() -> None:
    filename = get_unique_filename(
        filepath=pathlib.Path("get_template.json"), overwrite_option=False
    )
    with open(filename, "w") as output_file:
        json.dump(
            {
                "dataset_url": (
                    "ftp://my.cmems-du.eu/Core/"
                    "IBI_MULTIYEAR_PHY_005_002/"
                    "cmems_mod_ibi_phy_my_0.083deg-3D_P1Y-m"
                ),
                "filter": "*01yav_200[0-2]*",
                "regex": False,
                "output_directory": "copernicusmarine_data",
                "show_outputnames": True,
                "force_service": "files",
                "force_download": False,
                "request_file": False,
                "overwrite_output_data": False,
                "overwrite_metadata_cache": False,
                "no_metadata_cache": False,
            },
            output_file,
            indent=4,
        )
    logger.info(f"Template created at: {filename}")
