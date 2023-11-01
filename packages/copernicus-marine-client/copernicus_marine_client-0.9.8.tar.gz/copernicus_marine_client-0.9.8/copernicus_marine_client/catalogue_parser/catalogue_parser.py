import asyncio
import logging
from dataclasses import dataclass
from enum import Enum
from importlib.metadata import version
from itertools import chain, groupby, repeat
from json import loads
from typing import Any, Dict, Iterable, List, Optional, Tuple, TypeVar, Union

import aiohttp
import nest_asyncio
import pystac
import requests
from cachier import cachier

from copernicus_marine_client.command_line_interface.exception_handler import (
    log_exception_debug,
)
from copernicus_marine_client.core_functions.utils import (
    DEFAULT_CLIENT_BASE_DIRECTORY,
    construct_query_params_for_marine_data_store_monitoring,
    construct_url_with_query_params,
    map_reject_none,
    next_or_raise_exception,
)

logger = logging.getLogger("copernicus_marine_root_logger")

_S = TypeVar("_S")
_T = TypeVar("_T")


class _ServiceName(str, Enum):
    MOTU = "motu"
    OPENDAP = "opendap"
    GEOSERIES = "arco-geo-series"
    TIMESERIES = "arco-time-series"
    FILES = "original-files"
    FTP = "ftp"
    WMS = "wms"
    WMTS = "wmts"


class _ServiceShortName(str, Enum):
    MOTU = "motu"
    OPENDAP = "opendap"
    GEOSERIES = "geoseries"
    TIMESERIES = "timeseries"
    FILES = "files"
    FTP = "ftp"
    WMS = "wms"
    WMTS = "wmts"


MARINE_DATA_STORE_STAC_BASE_URL = "https://stac.marine.copernicus.eu/metadata"
MARINE_DATA_STORE_STAC_ROOT_CATALOG_URL = (
    MARINE_DATA_STORE_STAC_BASE_URL + "/catalog.stac.json"
)
MARINE_DATA_STORE_STAC_BASE_URL_STAGING = (
    "https://stac-dta.marine.copernicus.eu/metadata"
)
MARINE_DATA_STORE_STAC_ROOT_CATALOG_URL_STAGING = (
    MARINE_DATA_STORE_STAC_BASE_URL_STAGING + "/catalog.stac.json"
)


@dataclass(frozen=True)
class _Service:
    service_name: _ServiceName
    short_name: _ServiceShortName

    def aliases(self) -> List[str]:
        return (
            [self.service_name.value, self.short_name.value]
            if self.short_name.value != self.service_name.value
            else [self.service_name.value]
        )

    def to_json_dict(self):
        return {
            "service_name": self.service_name.value,
            "short_name": self.short_name.value,
        }


class CopernicusMarineDatasetServiceType(_Service, Enum):
    MOTU = _ServiceName.MOTU, _ServiceShortName.MOTU
    OPENDAP = _ServiceName.OPENDAP, _ServiceShortName.OPENDAP
    GEOSERIES = _ServiceName.GEOSERIES, _ServiceShortName.GEOSERIES
    TIMESERIES = (
        _ServiceName.TIMESERIES,
        _ServiceShortName.TIMESERIES,
    )
    FILES = _ServiceName.FILES, _ServiceShortName.FILES
    FTP = _ServiceName.FTP, _ServiceShortName.FTP
    WMS = _ServiceName.WMS, _ServiceShortName.WMS
    WMTS = _ServiceName.WMS, _ServiceShortName.WMTS


def _service_type_from_web_api_string(
    name: str,
) -> CopernicusMarineDatasetServiceType:
    class WebApi(Enum):
        MOTU = "motu"
        OPENDAP = "opendap"
        GEOSERIES = "timeChunked"
        TIMESERIES = "geoChunked"
        FILES = "native"
        FTP = "ftp"
        WMS = "wms"
        WMTS = "wmts"

    web_api_mapping = {
        WebApi.MOTU: CopernicusMarineDatasetServiceType.MOTU,
        WebApi.OPENDAP: CopernicusMarineDatasetServiceType.OPENDAP,
        WebApi.GEOSERIES: CopernicusMarineDatasetServiceType.GEOSERIES,
        WebApi.TIMESERIES: CopernicusMarineDatasetServiceType.TIMESERIES,
        WebApi.FILES: CopernicusMarineDatasetServiceType.FILES,
        WebApi.FTP: CopernicusMarineDatasetServiceType.FTP,
        WebApi.WMS: CopernicusMarineDatasetServiceType.WMS,
        WebApi.WMTS: CopernicusMarineDatasetServiceType.WMTS,
    }

    return next_or_raise_exception(
        (
            service_type
            for service_web_api, service_type in web_api_mapping.items()
            if service_web_api.value == name
        ),
        ServiceNotHandled(name),
    )


class ServiceNotHandled(Exception):
    ...


@dataclass
class CopernicusMarineDatasetService:
    service_type: CopernicusMarineDatasetServiceType
    uri: str


@dataclass
class CopernicusMarineDatasetCoordinates:
    coordinates_id: str
    units: str
    minimum_value: Optional[float]
    maximum_value: Optional[float]
    step: Optional[float]
    values: Optional[str]


@dataclass
class CopernicusMarineDatasetVariable:
    short_name: str
    standard_name: str
    units: str
    bbox: Tuple[float, float, float, float]
    coordinates: list[CopernicusMarineDatasetCoordinates]


@dataclass
class CopernicusMarineProductDataset:
    dataset_id: str
    dataset_name: str
    services: list[CopernicusMarineDatasetService]
    variables: list[CopernicusMarineDatasetVariable]

    def get_available_service_types(
        self,
    ) -> list[CopernicusMarineDatasetServiceType]:
        return list(map(lambda service: service.service_type, self.services))

    def get_service_by_service_type(
        self, service_type: CopernicusMarineDatasetServiceType
    ):
        return next(
            service
            for service in self.services
            if service.service_type == service_type
        )


@dataclass
class CopernicusMarineProductProvider:
    name: str
    roles: list[str]
    url: str
    email: str


@dataclass
class CopernicusMarineProduct:
    title: str
    product_id: str
    thumbnail_url: str
    description: str
    production_center: str
    creation_datetime: Optional[str]
    modified_datetime: Optional[str]
    keywords: dict[str, str]
    datasets: list[CopernicusMarineProductDataset]


@dataclass
class CopernicusMarineCatalogue:
    products: list[CopernicusMarineProduct]

    def filter(self, tokens: list[str]):
        return filter_catalogue_with_strings(self, tokens)


def _get_marine_data_store_root_catalog(
    staging: bool = False,
) -> dict:
    # Pass custom query parameters for MDS's Monitoring
    # (note that here we don't have 'username', shall we pass it?)
    data_store_root_url = (
        MARINE_DATA_STORE_STAC_ROOT_CATALOG_URL
        if not staging
        else MARINE_DATA_STORE_STAC_ROOT_CATALOG_URL_STAGING
    )
    return requests.get(
        data_store_root_url,
        params=construct_query_params_for_marine_data_store_monitoring(),
    ).json()


def _get_marine_data_store_stac_collection_from_product_url(
    product_url: str,
) -> Union[pystac.Collection, None]:
    try:
        # Pass custom query parameters for MDS's Monitoring
        # (note that here we don't have 'username', shall we pass it?)
        return pystac.Collection.from_file(
            construct_url_with_query_params(
                product_url,
                construct_query_params_for_marine_data_store_monitoring(),
            )
        )
    except KeyError as exception:
        messages = ["spatial", "temporal"]
        if exception.args[0] not in messages:
            logger.error(exception)
            raise KeyError(exception.args) from exception
        return None


def _construct_copernicus_marine_service(
    stac_service_name, stac_asset
) -> Optional[CopernicusMarineDatasetService]:
    try:
        return CopernicusMarineDatasetService(
            service_type=_service_type_from_web_api_string(stac_service_name),
            uri=stac_asset.get_absolute_href(),
        )
    except ServiceNotHandled as service_not_handled:
        log_exception_debug(service_not_handled)
        return None


def _get_services(
    stac_assets_dict: dict[str, pystac.Asset],
) -> list[CopernicusMarineDatasetService]:
    return [
        dataset_service
        for stac_service_name, stac_asset in stac_assets_dict.items()
        if stac_asset.roles and "data" in stac_asset.roles
        if (
            dataset_service := _construct_copernicus_marine_service(
                stac_service_name, stac_asset
            )
        )
        is not None
    ]


def _get_coordinates(
    dimensions_cube: dict,
) -> dict[str, CopernicusMarineDatasetCoordinates]:
    def _create_coordinate(
        key: str, value: dict
    ) -> CopernicusMarineDatasetCoordinates:
        return CopernicusMarineDatasetCoordinates(
            coordinates_id="depth" if key == "elevation" else key,
            units=value.get("unit") or "",
            minimum_value=value["extent"][0] if "extent" in value else None,
            maximum_value=value["extent"][1] if "extent" in value else None,
            step=value.get("step"),
            values=value.get("values"),
        )

    coordinates_dict = {}
    for key, value in dimensions_cube.items():
        coordinates_dict[key] = _create_coordinate(key, value)
    return coordinates_dict


def _get_variables(
    stac_dataset: pystac.Item,
) -> list[CopernicusMarineDatasetVariable]:
    def _create_variable(
        variable_cube: dict[str, Any],
        bbox: tuple[float, float, float, float],
        coordinates_dict: dict[str, CopernicusMarineDatasetCoordinates],
    ) -> Union[CopernicusMarineDatasetVariable, None]:
        coordinates = variable_cube["dimensions"]
        return CopernicusMarineDatasetVariable(
            short_name=variable_cube["id"],
            standard_name=variable_cube["standardName"],
            units=variable_cube.get("unit") or "",
            bbox=bbox,
            coordinates=[coordinates_dict[key] for key in coordinates],
        )

    coordinates_dict = _get_coordinates(
        stac_dataset.properties["cube:dimensions"]
    )
    bbox = stac_dataset.bbox
    variables: list[Optional[CopernicusMarineDatasetVariable]] = []
    for var_cube in stac_dataset.properties["cube:variables"].values():
        variables += [_create_variable(var_cube, bbox, coordinates_dict)]
    return [var for var in variables if var]


def _construct_marine_data_store_dataset(
    stac_dataset: pystac.Item,
) -> CopernicusMarineProductDataset:
    dataset_id = stac_dataset.id.rsplit("_", maxsplit=1)[
        0
    ]  # Remove the tag e.g.: '_202211'
    return CopernicusMarineProductDataset(
        dataset_id=dataset_id,
        dataset_name=stac_dataset.properties["title"],
        services=_get_services(stac_dataset.get_assets()),
        variables=_get_variables(stac_dataset),
    )


def _construct_marine_data_store_product(
    stac_tuple: Tuple[pystac.Collection, list[pystac.Item]],
) -> CopernicusMarineProduct:
    stac_product, stac_datasets = stac_tuple
    datasets = map_reject_none(
        _construct_marine_data_store_dataset, stac_datasets
    )
    production_center = [
        provider.name
        for provider in stac_product.providers or []
        if "producer" in provider.roles
    ]

    production_center_name = production_center[0] if production_center else ""

    thumbnail = stac_product.assets and stac_product.assets.get("thumbnail")
    creation_datetime = (
        stac_product.extra_fields
        and stac_product.extra_fields.get("properties")
        and stac_product.extra_fields.get("properties", {}).get("creationDate")
    )
    modified_datetime = (
        stac_product.extra_fields
        and stac_product.extra_fields.get("properties")
        and stac_product.extra_fields.get("properties", {}).get("modifiedDate")
    )

    return CopernicusMarineProduct(
        title=stac_product.title or stac_product.id,
        product_id=stac_product.id,
        thumbnail_url=thumbnail.get_absolute_href() if thumbnail else "",
        description=stac_product.description,
        production_center=production_center_name,
        creation_datetime=creation_datetime or "",
        modified_datetime=modified_datetime or "",
        keywords=stac_product.keywords,
        datasets=sorted(
            [dataset for dataset in datasets],
            key=lambda dataset: dataset.dataset_id,
        ),
    )


def _create_item(link: pystac.Link) -> Union[pystac.Item, None]:
    try:
        # Pass custom query parameters for MDS's Monitoring
        # (note that here we don't have 'username', shall we pass it?)
        return pystac.Item.from_file(
            construct_url_with_query_params(
                link.get_absolute_href(),
                construct_query_params_for_marine_data_store_monitoring(),
            )
        )
    except pystac.STACError as exception:
        message = (
            "Invalid Item: If datetime is None, a start_datetime "
            + "and end_datetime must be supplied."
        )
        if exception.args[0] != message:
            logger.error(exception)
            raise pystac.STACError(exception.args)
        return None


def _fetch_stac_datasets(
    stac_product: pystac.Collection,
) -> Tuple[pystac.Collection, list[pystac.Item]]:
    return (
        stac_product,
        [
            stac_dataset
            for stac_dataset in map(
                _create_item, stac_product.get_item_links()
            )
            if stac_dataset
        ],
    )


def _retrieve_missing_marine_data_store_products(
    portal_backend: list[CopernicusMarineProduct],
    staging: bool = False,
) -> list[CopernicusMarineProduct]:
    marine_data_store_root_catalog = _get_marine_data_store_root_catalog(
        staging=staging,
    )

    products_from_marine_data_store_catalog = filter(
        lambda y: y["rel"] == "child", marine_data_store_root_catalog["links"]
    )
    products_from_backend_portal_catalog = [
        product.product_id for product in portal_backend
    ]

    stac_base_url = (
        MARINE_DATA_STORE_STAC_BASE_URL
        if not staging
        else MARINE_DATA_STORE_STAC_BASE_URL_STAGING
    )
    marine_data_store_products_not_in_portal_backend_catalog = map(
        lambda x: stac_base_url + "/" + x["href"],
        filter(
            lambda y: y["title"] not in products_from_backend_portal_catalog,
            products_from_marine_data_store_catalog,
        ),
    )

    marine_data_store_products_as_stac_collection: Iterable[
        pystac.Collection
    ] = map_reject_none(
        _get_marine_data_store_stac_collection_from_product_url,
        marine_data_store_products_not_in_portal_backend_catalog,
    )

    stac_raw_data = map(
        _fetch_stac_datasets, marine_data_store_products_as_stac_collection
    )
    products = map_reject_none(
        _construct_marine_data_store_product, stac_raw_data
    )

    return list(products)


def parse_catalogue(
    overwrite_metadata_cache: bool,
    no_metadata_cache: bool,
    staging: bool = False,
) -> CopernicusMarineCatalogue:
    logger.debug("Parsing catalogue...")
    catalog = _parse_catalogue(
        overwrite_cache=overwrite_metadata_cache,
        ignore_cache=no_metadata_cache,
        _version=version("copernicus-marine-client"),
        staging=staging,
    )
    logger.debug("Catalogue parsed")
    return catalog


@cachier(cache_dir=DEFAULT_CLIENT_BASE_DIRECTORY)
def _parse_catalogue(
    _version: str,  # force cachier to overwrite cache in case of version update
    staging: bool = False,
) -> CopernicusMarineCatalogue:
    if not staging:
        logger.debug("Parsing portal catalogue...")
        portal_backend_catalog = _parse_portal_backend_catalogue()
        logger.debug("Portal catalogue parsed")
    else:
        # because of data misalignment we don't want to use data-be endpoint
        portal_backend_catalog = CopernicusMarineCatalogue(products=[])

    marine_data_store_missing_products = (
        _retrieve_missing_marine_data_store_products(
            portal_backend=portal_backend_catalog.products,
            staging=staging,
        )
    )

    return CopernicusMarineCatalogue(
        products=sorted(
            portal_backend_catalog.products
            + marine_data_store_missing_products,
            key=lambda product: product.product_id,
        )
    )


async def _async_fetch_raw_product(session, product_id: str):
    async with session.get(product_url(product_id)) as resp:
        text_response = await resp.text()
        return loads(text_response)


async def _async_fetch_raw_products(product_ids: List[str]):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for product_id in product_ids:
            tasks.append(
                asyncio.ensure_future(
                    _async_fetch_raw_product(session, product_id)
                )
            )

        return await asyncio.gather(*tasks)


def _fetch_raw_products() -> list[dict[str, Any]]:
    base_url = "https://data-be-prd.marine.copernicus.eu/api/datasets"
    response = requests.post(
        base_url,
        json={"size": 1000, "includeOmis": True},
    )
    assert response.ok, response.text
    raw_catalogue: dict[str, Any] = loads(response.text)

    nest_asyncio.apply()
    loop = asyncio.get_event_loop()

    results = loop.run_until_complete(
        _async_fetch_raw_products(raw_catalogue["datasets"].keys())
    )
    return results


def product_url(product_id: str) -> str:
    base_url = "https://data-be-prd.marine.copernicus.eu/api/dataset"
    return f"{base_url}/{product_id}" + "?variant=detailed-v2"


def variable_title_to_standard_name(variable_title: str) -> str:
    return variable_title.lower().replace(" ", "_")


def variable_to_pick(layer: dict[str, Any]) -> bool:
    return (
        layer["variableId"] != "__DEFAULT__"
        and layer["subsetVariableIds"]
        and len(layer["subsetVariableIds"]) == 1
    )


def _to_service(
    service_name: str, service_url: str
) -> Optional[CopernicusMarineDatasetService]:
    try:
        service_type = _service_type_from_web_api_string(service_name)
        return CopernicusMarineDatasetService(
            service_type=service_type, uri=service_url
        )
    except ServiceNotHandled as service_not_handled:
        log_exception_debug(service_not_handled)
        return None


def to_coordinates(
    subset_attributes: Tuple[str, dict[str, Any]], layer: dict[str, Any]
) -> CopernicusMarineDatasetCoordinates:
    coordinate_name = subset_attributes[0]
    values: Optional[str]
    if coordinate_name == "depth":
        values = layer.get("zValues")
    elif coordinate_name == "time":
        values = layer.get("tValues")
    else:
        values = None
    return CopernicusMarineDatasetCoordinates(
        coordinates_id=subset_attributes[0],
        units=subset_attributes[1]["units"],
        minimum_value=subset_attributes[1]["min"],
        maximum_value=subset_attributes[1]["max"],
        step=subset_attributes[1].get("step"),
        values=values,
    )


def portal_to_service(
    service_uri: Tuple[str, str]
) -> Optional[CopernicusMarineDatasetService]:
    return _to_service(service_uri[0], service_uri[1])


def to_variable(layer: dict[str, Any]) -> CopernicusMarineDatasetVariable:
    return CopernicusMarineDatasetVariable(
        short_name=layer["variableId"],
        standard_name=variable_title_to_standard_name(layer["variableTitle"]),
        units=layer["units"],
        bbox=layer["bbox"],
        coordinates=list(
            map(to_coordinates, layer["subsetAttrs"].items(), repeat(layer))
        ),
    )


def stac_to_service(asset) -> Optional[CopernicusMarineDatasetService]:
    return _to_service(asset[0], asset[1]["href"])


@dataclass
class DistinctDataset:
    dataset_id: str
    layer_elements: Iterable
    raw_services: Dict
    stac_items_values: Optional[Dict]


def to_dataset(
    distinct_dataset: DistinctDataset,
) -> CopernicusMarineProductDataset:
    dataset_id = distinct_dataset.dataset_id
    layer_elements = list(distinct_dataset.layer_elements)
    services_portal = list(
        map_reject_none(
            portal_to_service,
            distinct_dataset.raw_services.items(),
        ),
    )
    services_stac = (
        list(
            map_reject_none(
                stac_to_service,
                distinct_dataset.stac_items_values["assets"].items(),
            ),
        )
        if distinct_dataset.stac_items_values
        else []
    )

    services = list(chain(services_portal, services_stac))

    return CopernicusMarineProductDataset(
        dataset_id=dataset_id,
        dataset_name=layer_elements[0]["subdatasetTitle"],
        services=services,
        variables=list(
            map(to_variable, filter(variable_to_pick, layer_elements))
        ),
    )


def construct_unique_dataset(
    group_layer, raw_services, stac_items
) -> DistinctDataset:
    dataset_id_from_layer = group_layer[0]
    dataset_layer_elements = group_layer[1]
    dataset_raw_services = raw_services[dataset_id_from_layer]

    for stac_dataset_id, stac_items_values in stac_items.items():
        if stac_dataset_id.startswith(dataset_id_from_layer):
            if "--ext--" in stac_dataset_id.split(dataset_id_from_layer)[-1]:
                continue
            else:
                return DistinctDataset(
                    dataset_id=dataset_id_from_layer,
                    layer_elements=dataset_layer_elements,
                    raw_services=dataset_raw_services,
                    stac_items_values=stac_items_values,
                )
    else:
        return DistinctDataset(
            dataset_id=dataset_id_from_layer,
            layer_elements=dataset_layer_elements,
            raw_services=dataset_raw_services,
            stac_items_values=None,
        )


def to_datasets(
    raw_services: dict[str, dict[str, str]],
    layers: dict[str, dict[str, Any]],
    stac_items: dict,
) -> list[CopernicusMarineProductDataset]:
    groups_layers = groupby(
        layers.values(), key=lambda layer: layer["subdatasetId"]
    )
    distinct_datasets = map(
        construct_unique_dataset,
        groups_layers,
        repeat(raw_services),
        repeat(stac_items),
    )

    return sorted(
        map(to_dataset, distinct_datasets),
        key=lambda distinct_dataset: distinct_dataset.dataset_id,
    )


def _parse_product(raw_product: dict[str, Any]) -> CopernicusMarineProduct:
    return CopernicusMarineProduct(
        title=raw_product["title"],
        product_id=raw_product["id"],
        thumbnail_url=raw_product["thumbnailUrl"],
        description=raw_product["abstract"],
        production_center=raw_product["originatingCenter"],
        creation_datetime=raw_product.get("creationDate"),
        modified_datetime=raw_product.get("modifiedDate"),
        keywords=raw_product["keywords"],
        datasets=to_datasets(
            raw_product["services"],
            raw_product["layers"],
            raw_product["stacItems"],
        ),
    )


def _parse_portal_backend_catalogue() -> CopernicusMarineCatalogue:
    raw_products: list[dict[str, Any]] = _fetch_raw_products()

    return CopernicusMarineCatalogue(
        products=list(map(_parse_product, raw_products))
    )


# ---------------------------------------
# --- Utils function on any catalogue ---
# ---------------------------------------


def get_dataset_from_id(
    catalogue: CopernicusMarineCatalogue, dataset_id: str
) -> CopernicusMarineProductDataset:
    for product in catalogue.products:
        for dataset in product.datasets:
            if dataset_id == dataset.dataset_id:
                return dataset
    error = KeyError(
        f"The requested dataset '{dataset_id}' was not found in the catalogue,"
        " you can use 'copernicus-marine describe --include-datasets "
        "--contains <search_token>' to find datasets"
    )
    raise error


def get_dataset_and_suffix_path_from_url(
    catalogue: CopernicusMarineCatalogue, dataset_url: str
) -> Tuple[CopernicusMarineProductDataset, str]:
    return next_or_raise_exception(
        (
            dataset_and_suffix_url
            for product in catalogue.products
            for dataset in product.datasets
            for service in dataset.services
            if (
                dataset_and_suffix_url := _parse_dataset_and_suffix_url(
                    dataset, service.uri, dataset_url
                )
            )
            is not None
        ),
        KeyError(
            f"The requested dataset URL '{dataset_url}' "
            "was not found in the catalogue, "
            "you can use 'copernicus-marine describe --include-datasets "
            "--contains <search_token>' to find datasets"
        ),
    )


def _parse_dataset_and_suffix_url(
    dataset, service_uri, dataset_url
) -> Optional[Tuple[CopernicusMarineProductDataset, str]]:
    return (
        (dataset, dataset_url.split(service_uri)[1])
        if dataset_url.startswith(service_uri)
        else None
    )


def get_product_from_url(
    catalogue: CopernicusMarineCatalogue, dataset_url: str
) -> CopernicusMarineProduct:
    """
    Return the product object, with its dataset list filtered
    """
    filtered_catalogue = filter_catalogue_with_strings(
        catalogue, [dataset_url]
    )
    if filtered_catalogue is None:
        error = TypeError("filtered catalogue is empty")
        raise error
    if isinstance(filtered_catalogue, CopernicusMarineCatalogue):
        return filtered_catalogue.products[0]
    return filtered_catalogue["products"][0]


def filter_catalogue_with_strings(
    catalogue: CopernicusMarineCatalogue, tokens: list[str]
) -> dict[str, Any]:
    return find_match_object(catalogue, tokens) or {}


def find_match_object(value: Any, tokens: list[str]) -> Any:
    match: Any
    if isinstance(value, str):
        match = find_match_string(value, tokens)
    elif isinstance(value, Enum):
        match = find_match_enum(value, tokens)
    elif isinstance(value, tuple):
        match = find_match_tuple(value, tokens)
    elif isinstance(value, list):
        match = find_match_list(value, tokens)
    elif hasattr(value, "__dict__"):
        match = find_match_dict(value, tokens)
    else:
        match = None
    return match


def find_match_string(string: str, tokens: list[str]) -> Optional[str]:
    return string if any(token in string for token in tokens) else None


def find_match_enum(enum: Enum, tokens: list[str]) -> Any:
    return find_match_object(enum.value, tokens)


def find_match_tuple(tuple: Tuple, tokens: list[str]) -> Optional[list[Any]]:
    return find_match_list(list(tuple), tokens)


def find_match_list(object_list: list[Any], tokens) -> Optional[list[Any]]:
    def find_match(element: Any) -> Optional[Any]:
        return find_match_object(element, tokens)

    filtered_list: list[Any] = list(map_reject_none(find_match, object_list))
    return filtered_list if filtered_list else None


def find_match_dict(
    structure: dict[str, Any], tokens
) -> Optional[dict[str, Any]]:
    filtered_dict = {
        key: find_match_object(value, tokens)
        for key, value in structure.__dict__.items()
        if find_match_object(value, tokens)
    }

    found_match = any(filtered_dict.values())
    if found_match:
        new_dict = dict(structure.__dict__, **filtered_dict)
        structure.__dict__ = new_dict
    return structure if found_match else None
