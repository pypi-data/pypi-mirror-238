from typing import Callable, Union

import pandas
import xarray

from copernicus_marine_client.catalogue_parser.catalogue_parser import (
    CopernicusMarineDatasetServiceType,
    parse_catalogue,
)
from copernicus_marine_client.catalogue_parser.request_structure import (
    LoadRequest,
)
from copernicus_marine_client.core_functions.credentials_utils import (
    get_username_password,
)
from copernicus_marine_client.core_functions.services_utils import (
    CommandType,
    get_dataset_service_and_suffix_path,
)


def load_data_object_from_load_request(
    load_request: LoadRequest,
    arco_series_load_function: Callable,
    opendap_load_function: Callable,
) -> Union[xarray.Dataset, pandas.DataFrame]:
    catalogue = parse_catalogue(
        overwrite_metadata_cache=load_request.overwrite_metadata_cache,
        no_metadata_cache=load_request.no_metadata_cache,
    )
    dataset_service, _ = get_dataset_service_and_suffix_path(
        catalogue=catalogue,
        dataset_id=load_request.dataset_id,
        dataset_url=load_request.dataset_url,
        force_service_type=load_request.force_service,
        command_type=CommandType.LOAD,
        dataset_subset=load_request.get_time_and_geographical_subset(),
    )
    username, password = get_username_password(
        load_request.username,
        load_request.password,
        load_request.credentials_file,
    )
    load_request.dataset_url = dataset_service.uri
    if dataset_service.service_type in [
        CopernicusMarineDatasetServiceType.GEOSERIES,
        CopernicusMarineDatasetServiceType.TIMESERIES,
    ]:
        dataset = arco_series_load_function(
            username=username,
            password=password,
            dataset_url=load_request.dataset_url,
            variables=load_request.variables,
            geographical_parameters=load_request.geographical_parameters,
            temporal_parameters=load_request.temporal_parameters,
            depth_parameters=load_request.depth_parameters,
            chunks=None,
        )
    elif (
        dataset_service.service_type
        == CopernicusMarineDatasetServiceType.OPENDAP
    ):
        dataset, _ = opendap_load_function(
            username=username,
            password=password,
            dataset_url=load_request.dataset_url,
            variables=load_request.variables,
            geographical_parameters=load_request.geographical_parameters,
            temporal_parameters=load_request.temporal_parameters,
            depth_parameters=load_request.depth_parameters,
        )
    return dataset
