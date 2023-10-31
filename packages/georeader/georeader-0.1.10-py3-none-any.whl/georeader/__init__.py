from georeader.handlers.wfs_handler import WFSHandler
from georeader.handlers.esri_rest_handler import EsriRestHandler
from georeader.handlers.zipped_handler import ZippedHandler
from georeader.handlers.layer_handler import LayerHandler
from georeader.logic.error_exceptions import UnsupportedFormat, NotValid
from georeader.handlers.helpers.handlers import valid_file_types, valid_zip_types, valid_service_types, valid_db_types
from georeader.handlers.helpers.handlers import get_handler_file, get_handler_service, get_handler_zip, get_handler_db
from georeader.logic.error_exceptions import LayerDoesNotExist
from typing import List
import validators
import traceback
import os
import pathlib
import magic
import logging

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class GeoReader:
    def __init__(self, source: str, data_type: str = None):
        """A Class used to read spatial data"""
        self.data = None
        self.source = source
        self.handler_set = False
        self.data_type = self.get_data_type(source, data_type)
        if self.handler_set is False:
            self.handler = self.get_handler()(source)
        self.layers = self._get_layers()
        self.accepted_types = self.get_accepted_all_types()

    @staticmethod
    def get_accepted_file_types() -> list:
        return valid_zip_types

    @staticmethod
    def get_accepted_service_types() -> list:
        return valid_service_types

    @staticmethod
    def get_accepted_zip_types() -> list:
        return valid_service_types

    @staticmethod
    def get_accepted_db_types() -> list:
        return valid_db_types

    @staticmethod
    def get_accepted_all_types() -> list:
        return [*valid_zip_types, *valid_service_types, *valid_db_types, *valid_file_types]

    @staticmethod
    def create_pg_connection_str(db_name: str, db_user: str, db_pass: str, db_host: str = 'localhost'):
        return f"PG:dbname='{db_name}' user='{db_user}' password='{db_pass}' host='{db_host}'"

    @staticmethod
    def get_type_options():
        return {"zip": valid_zip_types,
                "service": valid_service_types,
                "file": valid_file_types,
                "db": valid_db_types
                }

    def get_handler(self):
        if self.data_type['type'] == 'service':
            handler = get_handler_service(self.data_type['name'])
        elif self.data_type['type'] == 'database':
            handler = get_handler_db(self.data_type['name'])
        elif self.data_type['type'] == 'file':
            handler = get_handler_file(self.data_type['name'])
        elif self.data_type['type'] == 'zip':
            handler = get_handler_zip(self.data_type['name'])
        else:
            raise ValueError(f"{self.data_type['type']} is not a supported format.")
        return handler

    def get_data_type(self, source: str, _type: str = None):
        """takes in a url or file and first tries to figure out first
        if it is a link (url) or a file (file_path) then will it will
        try to match up with one valid type.

        valid urls are web feature services or esri rest services
        valid file types currently are geopackage, geojson, json,
        shape files, gml, csv and zip files that contain one valid.

        Args:
            source (str): hopefully a valid url or a valid file path with ext
            _type (str): type of file or service
        Returns:
            [dict]: { "type": "url", "name": wfs }
            type_options = [ "url", "file_path", "unknown" ]
            name_options = [ "gpkg", "geojson", "json", "shp",
            "gml", "csv", "zip: <name_of_valid_file>" ]
        """
        data_type = {"type": "unknown", "name": "unknown"}
        if _type is not None:
            if _type in self.get_accepted_file_types():
                data_type = {"type": "file", "name": _type}
            elif _type in self.get_accepted_zip_types():
                data_type = {"type": "zip", "name": _type}
            elif _type in self.get_accepted_service_types():
                data_type = {"type": "service", "name": _type}
            elif _type in self.get_accepted_db_types():
                data_type = {"type": "db", "name": _type}
        else:
            if source.startswith("PG:"):
                data_type["type"] = "database"
                data_type['name'] = "postgresql"
            elif validators.url(source):
                data_type["type"] = "service"
                try:
                    handler = WFSHandler(source)
                    self.handler_set = True
                    self.handler = handler
                    data_type["name"] = "wfs"
                except NotValid:
                    pass
                if data_type["name"] != "wfs":
                    try:
                        handler = EsriRestHandler(source)
                        self.handler_set = True
                        self.handler = handler
                        data_type["name"] = "esri_rest"
                    except NotValid:
                        pass
                if data_type["name"] not in ["wfs", "esri_rest"]:
                    raise Exception("cannot get url type")
            elif os.path.exists(source):
                path_ext = pathlib.Path(source).suffix.split(".")[-1]
                data_type["name"] = path_ext
                if data_type["name"] in valid_zip_types:
                    data_type["type"] = "zip"
                elif data_type["name"] in valid_file_types:
                    data_type["type"] = "file"
                if os.path.isfile(source):
                    mime = magic.Magic(mime=True)
                    mimetype = mime.from_file(source)
                    data_type["mime_type"] = mimetype
            else:
                raise Exception(f"Error: {source} does not exist")

        if data_type["name"] not in self.get_accepted_all_types():
            _supported_data_types = ", ".join(self.get_accepted_all_types())
            _message = (
                f"{data_type['name']} is not a supported format."
                f"supported spatial data formats are {_supported_data_types}"
            )
            raise UnsupportedFormat(self.__init__, _message)
        return data_type

    def _get_layers(self) -> List[LayerHandler]:
        layers: List[LayerHandler] = []
        if isinstance(self.handler, ZippedHandler):
            handler_list = self._recursive_zip(self.handler, [])
            for handler_object in handler_list:
                for layer in handler_object.get_layers():
                    layer_object = LayerHandler(handler_object, layer['name'])
                    layers.append(layer_object)
        elif isinstance(self.handler, EsriRestHandler):
            for layer in self.handler.get_layers():
                layer_object = LayerHandler(self.handler, layer['name'])
                layers.append(layer_object)
        else:
            for layer in self.handler.get_layers():
                layer_object = LayerHandler(self.handler, layer['name'])
                layers.append(layer_object)
        return layers

    def _recursive_zip(self, zip_handler, past_handlers):
        for key, handler in zip_handler.handlers.items():
            if isinstance(handler, ZippedHandler):
                self._recursive_zip(handler, past_handlers)
            else:
                past_handlers.append(handler)
        return past_handlers

    def get_layer_count(self):
        return self.handler.get_layer_count()

    def list_layers(self):
        return [x.get_layer_name() for x in self.layers]

    def get_layers(self):
        return self.layers

    def get_layer(self, layer_name: str):
        layer_name: str = str(layer_name)
        for layer in self.layers:
            if layer.get_layer_name() == layer_name:
                return layer
