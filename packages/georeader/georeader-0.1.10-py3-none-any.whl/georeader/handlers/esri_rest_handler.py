import requests
import geopandas as gpd
import logging
from typing import Union
from urllib.parse import urljoin
from georeader.handlers.base_handler import BaseHandler
from georeader.logic.ogr.data_source import OGR_DataSource
from georeader.logic.main_helpers import get_json_safely
from urllib.parse import urlsplit
from functools import reduce
from georeader.logic.error_exceptions import NotValid
from shapely.geometry import Point
from georeader.logic.main_helpers import get_item_from_nested_dict


LOGGER = logging.getLogger("__name__")

ACCEPTED_LAYER_TYPES = ("feature layer", "group layer")
ACCEPTED_SERVICE_TYPES = ("MapServer", "FeatureServer")


def get_crs_from_spatial_ref(_spatial_ref) -> Union[str, None]:
    _crs_code = None
    for option in "latestWkid", "wkid":
        if option in _spatial_ref:
            _crs_code = _spatial_ref[option]
            break
    return _crs_code


class EsriRestHandler(BaseHandler):
    """handler for esri rest services"""

    handler_type = "esri_rest"
    source_type = "service"

    def __init__(self, url: str, preferred_crs: str = "27700"):
        """Handler for esri rest services.

        Args:
            url (str): [description]
            where (str, optional): [description]. Defaults to '1=1'.
        """
        self.url = url
        self.preferred_crs = preferred_crs
        self.base_url = self._get_base_url()
        self._params = self._get_params()
        self._routes = self._get_route(url)
        self.formatted_url = self.get_request_url()
        self.metadata = None
        self.type = None
        self.layers = None
        self.services = {}
        if not self.check_valid():
            raise NotValid(
                self.check_valid,
                f"{url} does not appear to be a valid ESRI rest service",
            )
        LOGGER.debug("initializing EsriRestHandler")
        LOGGER.debug(vars(self))

    @staticmethod
    def filter_out_operations_from_route(routes):
        """filter out esri operations from url
        Args:
            routes ([sting]): list of strings
        Returns:
            ([sting]): list of strings
        """
        possible_operations = [
            "layers",
            "legends",
            "query",
            "dynamic_layer",
            "uploads",
            "export",
            "identity",
            "find",
        ]
        if len(routes) == 0:
            return routes
        if routes[-1] in possible_operations:
            routes.remove(routes[-1])
        return routes

    @staticmethod
    def _count_request_params() -> dict:
        """return total number of features within layer

        Returns:
            str: esri rest params string
        """
        params = dict(returnCountOnly="true", where="1=1", f="json")
        return params

    def _get_base_url(self) -> str:
        """gets base url for esri rest service.

        Returns:
            str: [description]
        """
        if "rest/services" in self.url:
            return f"{self.url.split('rest/services')[0]}rest/services"
        else:
            split_url = urlsplit(self.url)
            return f"{split_url.scheme}://{split_url.netloc}"

    def _get_params(self) -> list:
        if "?" in self.url and self.url.split("?")[1].strip != "":
            params = self.url.split("?")[1].split("&")
            return [{"key": p.split("=")[0], "value": p.split("=")[1]} for p in params]
        return []

    def _get_supported_query_formats(self, service_name) -> list:
        """returns list of supported query formats

        Returns:
            list: list of support formats
        """
        pass

    def _get_route(self, url) -> list:
        item = url.split(self._get_base_url())
        if "?" in item[1]:
            item = item[1].split("?")[0]
        else:
            item = item[1]
        routes = list(filter(None, item.split("/")))
        routes = self.filter_out_operations_from_route(routes)
        return routes

    def get_service_urls(self):
        """finds esri route if valid.

        Returns:
            dict[str, str] | None: returns route if possible
        """
        routes = self._routes
        url_map = {
            "layer_or_group_url": None,
            "service_url": None,
            "base_url": self.base_url,
        }

        for idx, value in enumerate(routes):
            if value in ACCEPTED_SERVICE_TYPES:
                if len(routes) - 1 > idx and routes[idx + 1].isnumeric():
                    url_map[
                        "service_url"
                    ] = f"{self.base_url}/{'/'.join(routes[0:idx])}/{value}"
                    url_map[
                        "layer_or_group_url"
                    ] = f"{url_map['service_url']}/{routes[idx + 1]}"
                else:
                    url_map[
                        "service_url"
                    ] = f"{self.base_url}/{'/'.join(routes[0:idx])}/{value}"
        return url_map

    def get_request_url(self) -> str:
        url_dict = self.get_service_urls()
        for x in ["layer_or_group_url", "service_url", "base_url"]:
            if url_dict[x] is not None:
                return url_dict[x]

    def _query_request_params(self, request_format: str = "json", **kwargs) -> dict:
        """creates params from querying esri rest layer

        Args:
            request_format (str, optional): [description]. Defaults to 'json'.
            result_offset (int, optional): [description]. Defaults to 0.

        Returns:
            str: esri rest params string
        """
        if self.preferred_crs is not None:
            kwargs["outSR"] = self.preferred_crs
        params = dict(
            f=request_format,
            orderByFileds="OBJECTID+ASC",
            outFields="*",
            where="1=1",
            **kwargs,
        )
        return params

    def _get_layer_url(self, layer_name: str) -> str:
        layer_count = self.get_layer_count()
        if layer_count > 0:
            if layer_count != 1 and layer_name is None:
                raise Exception(
                    "Layer name or ID must be provided if more than one layer exist"
                )
            elif layer_count == 1 and layer_name is None:
                layer = self.layers[0]
                print(f"{layer['service_url']}/{layer['layer_id']}")
                return f"{layer['service_url']}/{layer['layer_id']}"
            else:
                layer_name = str(layer_name)
                for layer in self.layers:
                    if layer["layer_name"].lower() == layer_name.lower():
                        return f"{layer['service_url']}/{layer['layer_id']}"
                raise Exception(
                    f"Error: No Layers in service match name: '{layer_name}'"
                )
        else:
            raise Exception("no layers found in esri rest service")

    def get_esri_route_type(self, data_dict: dict) -> str:
        """get type from esri rest url
        Args:
            data_dict (Dictionary): Esri rest data
        Returns:
            String: type of rest url e.g. Feature Layer, Group Layer, Folder
        """

        if "error" in data_dict.keys():
            return "Error"
        if len(self._routes) > 0:
            if self._routes[-1].isnumeric():
                route_type = data_dict.get("type", None)
                if self._routes[-2].lower() in list(
                    map(lambda x: x.lower(), ACCEPTED_SERVICE_TYPES)
                ):
                    if route_type == "Feature Layer":
                        return "Feature Layer"
                    elif route_type == "Group Layer":
                        return "Group Layer"
                    else:
                        raise Exception(f"{route_type} is not currently supported")

                else:
                    raise Exception("Only ESRI FeatureServer and MapServer can be used")
            if "serviceDescription" in data_dict.keys() or self._routes[
                -1
            ].lower() in list(map(lambda x: x.lower(), ACCEPTED_SERVICE_TYPES)):
                for route in self._routes:
                    if route.lower() in list(
                        map(lambda x: x.lower(), ACCEPTED_SERVICE_TYPES)
                    ):
                        return "Service"
        elif "services" in data_dict.keys():
            return "Folder"
        return "Unknown"

    def _get_metadata(self):
        """
        The _get_metadata function is a helper function that returns the metadata for an esri service.
        It takes in a url and returns the metadata as a dictionary.

        Args:
            self: Reference the class instance

        Returns:
            A dictionary of the metadata for each layer in the service
        """

        def create_layer_object(_layer_data, _s_name, _s_url):
            return {
                "layer_name": f"{_s_name}/{_layer_data.get('name', '')}",
                "layer_name_short": _layer_data.get("name", ""),
                "layer_id": _layer_data.get("id", ""),
                "fields": _layer_data.get("fields", []),
                "extent": _layer_data.get("extent", ()),
                "service_name": _s_name,
                "service_url": _s_url,
                "layer_url": f"{_s_url}/{_layer_data.get('id', '')}"
            }

        def get_layers_from_service_data(_s_name, _s_url):
            if not _s_url.endswith("/"):
                _s_url = _s_url + "/"
            _s_layers_url = urljoin(_s_url, "layers")
            _resp = requests.get(_s_layers_url, params={"f": "json"})
            try:
                _s_layers_data = get_json_safely(_resp)
                return [
                    create_layer_object(_l_data, _s_name, _s_url)
                    for _l_data in _s_layers_data.get("layers", [])
                    if len(_l_data.get("subLayers", [])) == 0
                    and _l_data.get("type", "").lower()
                    in list(map(lambda x: x.lower(), ACCEPTED_LAYER_TYPES))
                ]
            except ValueError:
                return []

        def get_service_from_folder(_data, url):
            _services = []
            for _service in _data.get("services", []):
                if _service["type"].lower() in list(
                    map(lambda x: x.lower(), ACCEPTED_SERVICE_TYPES)
                ):
                    _service_url = reduce(
                        urljoin,
                        [
                            f"{self.base_url}/",
                            f'{_service["name"]}/',
                            f'{_service["type"]}/',
                        ],
                    )
                    # _resp = requests.get(_service_url, params={"f": "json"})
                    # _service_data = get_json_safely(_resp)
                    _services.append(
                        {
                            "service_name": _service["name"],
                            "service_url": _service_url,
                            # "service_metadata": _service_data,
                        }
                    )
            for _folder_name in _data.get("folders", []):
                _folder_url = f"{url}/{_folder_name}"
                try:
                    _resp = requests.get(_folder_url, params={"f": "json"})
                    _folder_data = get_json_safely(_resp)
                    _services += get_service_from_folder(_folder_data, _folder_url)
                except ValueError:
                    pass
            return _services

        request_url = self.formatted_url
        resp = requests.get(request_url, params={"f": "json"})
        data = get_json_safely(resp)
        url_type = self.get_esri_route_type(data)

        if url_type.lower() not in list(
            map(lambda x: x.lower(), ["folder", "service", *ACCEPTED_LAYER_TYPES])
        ):
            raise Exception("service or layer type is not allowed.")

        metadata = {}
        try:
            if url_type.lower() == "folder":
                layers = []
                services = get_service_from_folder(data, request_url)
                for service in services:
                    metadata[service["service_name"]] = service
                    layers += get_layers_from_service_data(
                        service["service_name"], service["service_url"]
                    )

            elif url_type.lower() == "service":
                service_url = self.get_service_urls().get("service_url")
                service_name = self._get_route(service_url)[-2]
                metadata[service_name] = {
                    "service_name": service_name,
                    "service_url": service_url,
                    # "service_metadata": data,
                }
                layers = get_layers_from_service_data(service_name, service_url)
            elif url_type.lower() in ACCEPTED_LAYER_TYPES:
                service_url = self.get_service_urls().get("service_url")
                resp = requests.get(service_url, params={"f": "json"})
                service_data = get_json_safely(resp)
                service_name = self._get_route(service_url)[-2]
                metadata[service_name] = {
                    "service_name": service_name,
                    "service_url": service_url,
                    "service_metadata": service_data,
                }
                if url_type.lower() == "group layer":
                    layers = [
                        create_layer_object(
                            sub_layer.get("name"), service_name, service_url
                        )
                        for sub_layer in data["subLayers"]
                    ]
                else:
                    layers = [create_layer_object(data, service_name, service_url)]
            self.metadata = metadata
            self.layers = layers
            for layer in layers:
                if layer["service_name"] in self.services.keys():
                    self.services[layer["service_name"]].append(layer)
                else:
                    self.services[layer["service_name"]] = [layer]

        except Exception as e:
            raise Exception("failed to get metadata") from e

    def check_valid(self) -> bool:
        """does some basic check to see if layer is valid.

        Returns:
            bool: [description]
        """

        try:
            self._get_metadata()
            return True
        except Exception as e:
            LOGGER.error(e)
            LOGGER.error(
                "Failed to get metadata for esri rest service. please check url is correct"
            )
            return False

    def get_max_record_count(self, layer_name: str) -> int:
        """
        The get_max_record_count function returns the maximum number of records that can be returned by a query.

        Args:
            self: Reference the object that is calling the function
            layer_name: str: Pass in the layer name

        Returns:
            The maximum number of records that can be returned by a query
        """

        layer_url = self._get_layer_url(layer_name)
        resp = requests.get(layer_url, params={"f": "json"})
        data = get_json_safely(resp)
        return data.get("maxRecordCount")

    def get_schema(self, layer_name: str = None) -> list:
        """
        The get_schema function returns a list of the fields in a layer.

        Args:
            self: Refer to the object itself
            layer_name: str: Pass in the layer name

        Returns:
            A list of the fields in a layer
        """

        layer_url = self._get_layer_url(layer_name)
        resp = requests.get(layer_url, params={"f": "json"})
        data = get_json_safely(resp)
        if data.get("fields") is not None:
            return [
                x.get("name")
                for x in data.get("fields")
                if x.get("type") != "esriFieldTypeGeometry"
            ]
        else:
            return []

    def get_feature_count(self, layer_name: str = None) -> int:
        query_url = f"{self._get_layer_url(layer_name)}/query"
        response = requests.get(query_url, params=self._count_request_params())
        return get_json_safely(response).get("count")

    def generate_sample_url_request(self, query_url):
        query_params = self._query_request_params(ResultRecordCount=1)
        request_url = (
            requests.Request("GET", query_url, params=query_params).prepare().url
        )
        return request_url

    def generate_request_urls(self, query_url) -> list:
        features_per_request = 1000
        total_size = self.get_feature_count()
        calls = total_size // features_per_request + 1
        request_urls = []
        for j in range(0, calls):
            offset = j * features_per_request
            query_params = self._query_request_params(
                resultOffset=offset, ResultRecordCount=features_per_request
            )
            request_url = (
                requests.Request("GET", query_url, params=query_params).prepare().url
            )
            request_urls.append(request_url)
        return request_urls

    def get_dataframe(self, layer_name: str = None) -> gpd.geodataframe:
        """
        The get_dataframe function returns a GeoPandas dataframe for the specified layer.

        Args:
            self: Represent the instance of the class
            layer_name: str: Specify the layer name or id that you want to get a dataframe for
        Returns:
            A geodataframe
        """
        ds = self.get_datastore_for_layer(layer_name)
        layer = ds.get_layer_by_name(ds.get_all_layer_names()[0])
        return layer.get_dataframe()

    def get_layer_count(self) -> int:
        """return layer count

        Returns:
            int: layer count
        """
        return len(self.layers)

    def get_layers(self) -> list:
        """return list of layers

        Returns:
            list: layer list
        """
        return [{'name': x["layer_name"]} for x in self.layers]

    def get_layer_id_by_name(self, layer_name):
        for layer in self.layers:
            if layer['layer_name'] == layer_name:
                return layer["layer_id"]
        return None

    def get_layer_name_by_id(self, layer_id, service_name):
        if len(self.handler.services) > 1 and service_name is None:
            raise Exception("Multiple Services detected, service_name required.")
        for layer in self.services[service_name]:
            if str(layer["layer_id"]) == str(layer_id):
                return layer["layer_name"]
        else:
            for layer in self.layers:
                if layer['layer_id'] == layer_id:
                    return layer["layer_name"]
        return None

    def _get_layer_metadata(self, layer_name):
        """return metadata for layer.
        Args:
            layer_name (str, optional): [description]. Defaults to None.

        Returns:
            list: list: return list of attribute names.
        """

        resp = requests.get(
            self._get_layer_url(layer_name),
            params={
                "f": "json",
            },
        )
        data = get_json_safely(resp)
        return data

    def get_extent(self, layer_name: str) -> tuple:
        """
            The get_extent function returns the extent of a layer in the preferred CRS.

            Args:
                self: Bind the method to the class
                layer_name: str: Specify the layer name or id of the layer to get metadata for

            Returns:
                A tuple with the xmin, xmax, ymin and ymax values of the extent
        """
        layer_metadata = self._get_layer_metadata(layer_name)
        spatial_ref = layer_metadata["extent"]["spatialReference"]
        crs_code = str(get_crs_from_spatial_ref(spatial_ref))
        esri_extend = layer_metadata["extent"]
        if self.preferred_crs == crs_code:
            return (
                esri_extend.get("xmin", 0),
                esri_extend.get("xmax", 0),
                esri_extend.get("ymin", 0),
                esri_extend.get("ymax", 0),
            )
        elif layer_metadata["currentVersion"] > 10.30:
            ds = self.get_datastore_for_layer(layer_name)
            layer_name = ds.get_all_layer_names()[0]
            extent = ds.get_layer_by_name(layer_name).get_extent()
            return extent
        else:
            extent_series = gpd.GeoSeries(
                [
                    Point(esri_extend.get("xmin", 0), esri_extend.get("ymin", 0)),
                    Point(esri_extend.get("xmax", 0), esri_extend("ymax", 0)),
                ]
            )
            extent_series = extent_series.set_crs(epsg=int(crs_code))
            extent_series = extent_series.to_crs(epsg=int(self.preferred_crs))
            extent = (
                extent_series[0].xy[0][0],
                extent_series[1].xy[0][0],
                extent_series[0].xy[1][0],
                extent_series[1].xy[1][0],
            )
            return extent

    def get_crs_code(self, layer_name: str):
        """
        The get_crs_code function is used to get the CRS code of a layer.
        The function takes in two parameters: layer_name and service name.
        It then uses the _get_layer metadata function to get the spatial reference of that particular layer,
        and then it gets the crs code from that spatial reference using another helper function called get_crs from spatial ref.

        Args:
            self: Refer to the object itself
            layer_name: str: Specify the layer name or id of a service

        Returns:
            A string that represents the coordinate system code
        """
        try:
            layer_metadata = self._get_layer_metadata(layer_name)
            spatial_ref = layer_metadata["extent"]["spatialReference"]
            crs_code = str(get_crs_from_spatial_ref(spatial_ref))
            if crs_code is None:
                raise ValueError("could not get crs code")
            if self.preferred_crs is not None and self.preferred_crs != crs_code:
                query_params = self._query_request_params(
                    resultOffset=0, ResultRecordCount=1
                )
                response = requests.get(
                    f"{self._get_layer_url(layer_name)}/query",
                    params=query_params,
                )
                resp_json = get_json_safely(response)
                crs_code = get_crs_from_spatial_ref(resp_json["spatialReference"])
            return crs_code
        except KeyError as e:
            return None

    def get_geom_type(self, layer_name: str):
        """return geom type as str
        Args:
            layer_name:
        Returns:
            str: returns geom type
        """
        layer_metadata = self._get_layer_metadata(layer_name)
        if "geometryType" in layer_metadata:
            return layer_metadata["geometryType"]
        else:
            return None

    def get_datastore_for_layer(self, layer_name: str = None) -> OGR_DataSource:
        """
        The get_datastore_for_layer function returns a GeoPandas DataFrame containing the data for a given layer.

        Args:
            self: Refer to the class instance itself
            layer_name: str: Specify the layer name or id of the feature service

        Returns:
            An ogr_datasource object
        """
        query_url = f"{self._get_layer_url(layer_name)}/query"
        query_params = self._query_request_params()
        request_url = (
            requests.Request("GET", query_url, params=query_params).prepare().url
        )
        data_source = OGR_DataSource(_input=request_url, _type="ESRIJSON")
        return data_source

    def write_to_postgis_db(
        self,
        layer_name: str,
        table_name: str,
        schema: str,
        connection_str: str,
        crs: int = None,
        overwrite: bool = False,
        force_type: int = None,
    ):

        if layer_name is None:
            raise Exception("provide name of layer")
        else:
            ds = self.get_datastore_for_layer(layer_name)
            layer = ds.get_layer_by_name(ds.get_all_layer_names()[0])
            layer.write_to_postgis_db(
                table_name=table_name,
                schema=schema,
                connection_string=connection_str,
                crs=crs,
                overwrite=overwrite,
                force_type=force_type,
            )
