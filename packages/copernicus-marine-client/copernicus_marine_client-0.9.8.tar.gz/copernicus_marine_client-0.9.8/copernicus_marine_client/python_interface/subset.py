import pathlib
from datetime import datetime
from typing import List, Optional, Union

from copernicus_marine_client.core_functions.deprecated import (
    deprecated_python_option,
)
from copernicus_marine_client.core_functions.deprecated_options import (
    DEPRECATED_OPTIONS,
)
from copernicus_marine_client.core_functions.subset import subset_function
from copernicus_marine_client.python_interface.exception_handler import (
    log_exception_and_exit,
)
from copernicus_marine_client.python_interface.utils import homogenize_datetime


@deprecated_python_option(**DEPRECATED_OPTIONS.dict_old_names_to_new_names)
@log_exception_and_exit
def subset(
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
    output_filename: Optional[Union[pathlib.Path, str]] = None,
    force_service: Optional[str] = None,
    request_file: Optional[Union[pathlib.Path, str]] = None,
    output_directory: Optional[Union[pathlib.Path, str]] = None,
    credentials_file: Optional[Union[pathlib.Path, str]] = None,
    motu_api_request: Optional[str] = None,
    force_download: bool = False,
    overwrite_output_data: bool = False,
    overwrite_metadata_cache: bool = False,
    no_metadata_cache: bool = False,
    staging: bool = False,
) -> pathlib.Path:
    """
    Extracts a subset of data from a specified dataset using given parameters.

    Args:
        dataset_url (str, optional): URL of the dataset source.
        dataset_id (str, optional): Identifier for the dataset.
        username (str, optional): Username for authentication.
        password (str, optional): Password for authentication.
        variables (List[str], optional): List of variable names to extract.
        minimum_longitude (float, optional): Minimum longitude value for spatial subset.
        maximum_longitude (float, optional): Maximum longitude value for spatial subset.
        minimum_latitude (float, optional): Minimum latitude value for spatial subset.
        maximum_latitude (float, optional): Maximum latitude value for spatial subset.
        minimum_depth (float, optional): Minimum depth value for vertical subset.
        maximum_depth (float, optional): Maximum depth value for vertical subset.
        vertical_dimension_as_originally_produced (bool, optional): Use original vertical dimension.
        start_datetime (datetime, optional): Start datetime for temporal subset.
        end_datetime (datetime, optional): End datetime for temporal subset.
        output_filename (Union[pathlib.Path, str], optional): Output filename/path for the subsetted data.
        force_service (str, optional): Force use of specified data service.
        request_file (Union[pathlib.Path, str], optional): Path to request file.
        output_directory (Union[pathlib.Path, str], optional): Directory to save output files.
        credentials_file (Union[pathlib.Path, str], optional): Path to credentials file.
        motu_api_request (str, optional): MOTU API request string.
        force_download (bool, optional): Skip confirmation before download.
        overwrite_output_data (bool, optional): Overwrite existing output data if True.
        overwrite_metadata_cache (bool, optional): Overwrite existing metadata cache if True.
        no_metadata_cache (bool, optional): Disable metadata caching if True.

    Returns:
        pathlib.Path: Path to the generated subsetted data file.
    """  # noqa
    output_filename = (
        pathlib.Path(output_filename) if output_filename else None
    )
    request_file = pathlib.Path(request_file) if request_file else None
    output_directory = (
        pathlib.Path(output_directory) if output_directory else None
    )
    credentials_file = (
        pathlib.Path(credentials_file) if credentials_file else None
    )

    start_datetime = homogenize_datetime(start_datetime)
    end_datetime = homogenize_datetime(end_datetime)

    return subset_function(
        dataset_url,
        dataset_id,
        username,
        password,
        variables,
        minimum_longitude,
        maximum_longitude,
        minimum_latitude,
        maximum_latitude,
        minimum_depth,
        maximum_depth,
        vertical_dimension_as_originally_produced,
        start_datetime,
        end_datetime,
        output_filename,
        force_service,
        request_file,
        output_directory,
        credentials_file,
        motu_api_request,
        force_download,
        overwrite_output_data,
        overwrite_metadata_cache,
        no_metadata_cache,
        staging=staging,
    )
