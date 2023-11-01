import logging
import pathlib
from datetime import datetime
from typing import List, Optional

import click

from copernicus_marine_client.command_line_interface.exception_handler import (
    log_exception_and_exit,
)
from copernicus_marine_client.command_line_interface.utils import (
    MutuallyExclusiveOption,
    assert_cli_args_are_not_set_except_create_template,
)
from copernicus_marine_client.core_functions.deprecated import (
    DeprecatedClickOption,
    DeprecatedClickOptionsCommand,
)
from copernicus_marine_client.core_functions.services_utils import CommandType
from copernicus_marine_client.core_functions.subset import (
    create_subset_template,
    subset_function,
)
from copernicus_marine_client.core_functions.utils import (
    DATETIME_SUPPORTED_FORMATS,
    OVERWRITE_LONG_OPTION,
    OVERWRITE_OPTION_HELP_TEXT,
    OVERWRITE_SHORT_OPTION,
)

logger = logging.getLogger("copernicus_marine_root_logger")


@click.group()
def cli_group_subset() -> None:
    pass


@cli_group_subset.command(
    "subset",
    cls=DeprecatedClickOptionsCommand,
    short_help="Download subsets of datasets as NetCDF files or Zarr stores",
    help="""
    Download subsets of datasets as NetCDF files or Zarr stores.

    Either one of --dataset-id or --dataset-url is required (can be found via the "describe" command).
    The arguments value passed individually through the CLI take precedence over the values from the --motu-api-request option,
    which takes precedence over the ones from the --request-file option
    """,  # noqa
    epilog="""
    Examples:

    \b
    copernicus-marine subset
    --dataset-id cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i
    --variable thetao
    --start-datetime 2022-01-01T00:00:00 --end-datetime 2022-12-31T23:59:59
    --minimum-longitude -6.17 --maximum-longitude -5.08
    --minimum-latitude 35.75 --maximum-latitude 36.30
    --minimum-depth 0.0 --maximum-depth 5.0

    \b
    copernicus-marine subset -i cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i -v thetao -t 2022-01-01T00:00:00 -T 2022-12-31T23:59:59 -x -6.17 -X -5.08 -y 35.75 -Y 36.30 -z 0.0 -Z 5.0
    """,  # noqa
)
@click.option(
    "--dataset-url",
    "-u",
    type=str,
    help="The full dataset URL.",
)
@click.option(
    "--dataset-id",
    "-i",
    type=str,
    help="The datasetID.",
)
@click.option(
    "--username",
    type=str,
    default=None,
    help="If not set, search for environment variable"
    + " COPERNICUS_MARINE_SERVICE_USERNAME"
    + ", or else look for configuration files, or else ask for user input.",
)
@click.option(
    "--password",
    type=str,
    default=None,
    help="If not set, search for environment variable"
    + " COPERNICUS_MARINE_SERVICE_PASSWORD"
    + ", or else look for configuration files, or else ask for user input.",
)
@click.option(
    "--variable",
    "-v",
    "variables",
    type=str,
    help="Specify dataset variables",
    multiple=True,
)
@click.option(
    "--minimum-longitude",
    "--minimal-longitude",
    "-x",
    cls=DeprecatedClickOption,
    deprecated=["--minimal-longitude"],
    preferred="--minimum-longitude",
    type=float,
    help=(
        "Minimum longitude for the subset. "
        "The value will be reduced to the interval [-180; 360[."
    ),
)
@click.option(
    "--maximum-longitude",
    "--maximal-longitude",
    "-X",
    cls=DeprecatedClickOption,
    deprecated=["--maximal-longitude"],
    preferred="--maximum-longitude",
    type=float,
    help=(
        "Maximum longitude for the subset. "
        "The value will be reduced to the interval [-180; 360[."
    ),
)
@click.option(
    "--minimum-latitude",
    "--minimal-latitude",
    "-y",
    cls=DeprecatedClickOption,
    deprecated=["--minimal-latitude"],
    preferred="--minimum-latitude",
    type=click.FloatRange(min=-90, max=90),
    help="Minimum latitude for the subset."
    " Requires a float within this range:",
)
@click.option(
    "--maximum-latitude",
    "--maximal-latitude",
    "-Y",
    cls=DeprecatedClickOption,
    deprecated=["--maximal-latitude"],
    preferred="--maximum-latitude",
    type=click.FloatRange(min=-90, max=90),
    help="Maximum latitude for the subset."
    " Requires a float within this range:",
)
@click.option(
    "--minimum-depth",
    "--minimal-depth",
    "-z",
    cls=DeprecatedClickOption,
    deprecated=["--minimal-depth"],
    preferred="--minimum-depth",
    type=click.FloatRange(min=0),
    help="Minimum depth for the subset. Requires a float within this range:",
)
@click.option(
    "--maximum-depth",
    "--maximal-depth",
    "-Z",
    cls=DeprecatedClickOption,
    deprecated=["--maximal-depth"],
    preferred="--maximum-depth",
    type=click.FloatRange(min=0),
    help="Maximum depth for the subset. Requires a float within this range:",
)
@click.option(
    "--vertical-dimension-as-originally-produced",
    type=bool,
    default=True,
    show_default=True,
    help=(
        "Consolidate the vertical dimension (the z-axis) as it is in the "
        "dataset originally produced, "
        "named `depth` with descending positive values."
    ),
)
@click.option(
    "--start-datetime",
    "-t",
    type=click.DateTime(DATETIME_SUPPORTED_FORMATS),
    help="The start datetime of the temporal subset. "
    "Caution: encapsulate date "
    + 'with " " to ensure valid expression for format "%Y-%m-%d %H:%M:%S".',
)
@click.option(
    "--end-datetime",
    "-T",
    type=click.DateTime(DATETIME_SUPPORTED_FORMATS),
    help="The end datetime of the temporal subset. Caution: encapsulate date "
    + 'with " " to ensure valid expression for format "%Y-%m-%d %H:%M:%S".',
)
@click.option(
    "--output-directory",
    "-o",
    type=click.Path(path_type=pathlib.Path),
    help="The destination folder for the downloaded files."
    + " Default is the current directory.",
)
@click.option(
    "--credentials-file",
    type=click.Path(path_type=pathlib.Path),
    help=(
        "Path to a credentials file if not in its default directory. "
        "Accepts .copernicus-marine-credentials / .netrc or _netrc / "
        "motuclient-python.ini files."
    ),
)
@click.option(
    "--output-filename",
    "-f",
    type=click.Path(path_type=pathlib.Path),
    help=(
        "Concatenate the downloaded data in the given file name "
        "(under the output directory). If "
        "the output-filename argument ends with '.nc' suffix,"
        " the file will be downloaded as a netCDF file."
    ),
)
@click.option(
    "--force-download",
    is_flag=True,
    default=False,
    help="Flag to skip confirmation before download.",
)
@click.option(
    OVERWRITE_LONG_OPTION,
    OVERWRITE_SHORT_OPTION,
    is_flag=True,
    default=False,
    help=OVERWRITE_OPTION_HELP_TEXT,
)
@click.option(
    "--force-service",
    "-s",
    type=str,
    help=(
        "Force download through one of the available services "
        f"using the service name among {CommandType.SUBSET.service_names()} "
        f"or its short name among {CommandType.SUBSET.service_short_names()}."
    ),
)
@click.option(
    "--create-template",
    type=bool,
    is_flag=True,
    default=False,
    help="Option to create a file subset_template.json in your current directory "
    "containing CLI arguments. If specify, no other action will be performed.",
)
@click.option(
    "--request-file",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Option to pass a file containing CLI arguments. "
    "The file MUST follow the structure of dataclass 'SubsetRequest'.",
)
@click.option(
    "--motu-api-request",
    type=str,
    help=(
        "Option to pass a complete MOTU api request as a string. "
        'Caution, user has to replace double quotes " with single '
        "quotes ' in the request."
    ),
)
@click.option(
    "--overwrite-metadata-cache",
    cls=MutuallyExclusiveOption,
    type=bool,
    is_flag=True,
    default=False,
    help="Force to refresh the catalogue by overwriting the local cache.",
    mutually_exclusive=["no_metadata_cache"],
)
@click.option(
    "--no-metadata-cache",
    cls=MutuallyExclusiveOption,
    type=bool,
    is_flag=True,
    default=False,
    help="Bypass the use of cache.",
    mutually_exclusive=["overwrite_metadata_cache"],
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL", "QUIET"]),
    default="INFO",
    help=(
        "Set the details printed to console by the command "
        "(based on standard logging library)."
    ),
)
@click.option(
    "--staging",
    type=bool,
    default=False,
    is_flag=True,
    hidden=True,
)
@log_exception_and_exit
def subset(
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
    create_template: bool,
    request_file: Optional[pathlib.Path],
    output_directory: Optional[pathlib.Path],
    credentials_file: Optional[pathlib.Path],
    motu_api_request: Optional[str],
    force_download: bool,
    overwrite_output_data: bool,
    overwrite_metadata_cache: bool,
    no_metadata_cache: bool,
    log_level: str,
    staging: bool = False,
):
    if log_level == "QUIET":
        logger.disabled = True
        logger.setLevel(level="CRITICAL")
    else:
        logger.setLevel(level=log_level)

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("DEBUG mode activated")

    if create_template:
        assert_cli_args_are_not_set_except_create_template(
            click.get_current_context()
        )
        create_subset_template()
        return

    subset_function(
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
        staging,
    )
