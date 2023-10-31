import geopandas as gpd
import os
import logging
from georeader.handlers.base_handler import BaseHandler
from georeader.logic.main_helpers import get_file_ext
from georeader.logic.ogr.data_source import OGR_DataSource
from typing import Any, Callable, Tuple, List
from georeader.handlers.helpers.directory_helper import DirectoryHelper
from georeader.logic.error_exceptions import NotValid

LOGGER = logging.getLogger("__name__")


class GeneralHandler(BaseHandler, DirectoryHelper):
    def __init__(self,
                 source: str,
                 gdal_drivers: List[str],
                 *args,
                 **kwargs):
        super(GeneralHandler, self).__init__()
        if self.source_type == "file":
            if os.path.exists(source):
                self.source = source
                self.file_extension = get_file_ext(self.source)
            else:
                raise ValueError(f"{source} path does not exist")
        else:
            self.source = source
        self._metadata = {}
        self._data_source = None
        self.GDAL_drivers = gdal_drivers
        if not self.check_valid():
            raise NotValid(
                self.check_valid,
                f"{source} does not appear to be a valid {self.handler_type} type",
            )
        LOGGER.debug("initializing GeneralHandler")
        LOGGER.debug(vars(self))

    def destroy(self):
        self._data_source.destroy()

    def restore(self):
        for driver in self.GDAL_drivers:
            data_source = OGR_DataSource(_input=self.source, _type=driver)
            if data_source.data_source_exist():
                self._data_source = data_source
                break

    def get_feature_count(self, layer_name: str = None) -> int:
        """return number of features

        Returns:
            int: feature count
        """
        return self.get_metadata_attribute("feature_count", layer_name)

    def get_crs_code(self, layer_name: str = None) -> str:
        """returns CRS code for layer.
        Args:
            layer_name:

        Returns:

        """
        return self.get_metadata_attribute("crs_code", layer_name)

    def get_extent(self, layer_name: str = None) -> Tuple[float]:
        """return extent for layer.
        Args:
            layer_name (str, optional): [description]. Defaults to None.
        Returns:
            Tuple: return max bounds of layer.
        """
        return self.get_metadata_attribute("extent", layer_name)

    def get_dataframe(self, layer_name: str = None) -> gpd.GeoDataFrame:
        """returns geopandas dataframe.

        Returns:
            gpd.GeoDataFrame:
        """
        return self._data_source.get_layer_by_name(layer_name).get_dataframe()

    def get_schema(self, layer_name: str = None) -> List[str]:
        """returns layer schema
        Args:
            layer_name (str, optional): name of layer if more than one layer exists. Defaults to None.
        Returns:
            List[str]: return list of attribute names.
        """
        return self.get_metadata_attribute("schema", layer_name)

    def get_file_name(self) -> str:
        """returns file name

        Returns:
            str: file name
        """
        return self.source

    def get_layer_count(self) -> int:
        """returns layer count.

        Returns:
            int: number of layers.
        """
        return len(self._metadata.keys())

    def get_layers(self) -> List[str]:
        """return list of layers

        Returns:
            List[str]: layer list
        """
        return [{"name": x} for x in self._metadata.keys()]

    def get_geom_type(self, layer_name: str = None) -> str:
        """returns geom type for layer
        Returns:
            str: name of geom type e.g polygon, point...
        """
        return self.get_metadata_attribute("geom_type", layer_name)

    def write_to_postgis_db(self,
                            layer_name: str,
                            table_name: str,
                            schema: str,
                            connection_str: str,
                            crs: int = None,
                            overwrite: bool = False,
                            force_type: int = None
                            ):

        if layer_name is None:
            raise Exception("provide name of layer")
        else:
            ogr_layer = self._data_source.get_layer_by_name(layer_name)
            ogr_layer.write_to_postgis_db(
                table_name=table_name,
                schema=schema,
                connection_string=connection_str,
                crs=crs,
                overwrite=overwrite,
                force_type=force_type,
            )

    def _set_metadata(self):
        for driver in self.GDAL_drivers:
            data_source = OGR_DataSource(_input=self.source, _type=driver)
            if data_source.data_source_exist():
                self._data_source = data_source
                break
        if self._data_source is None:
            raise ValueError("Failed to read file")
        for layer_name in self._data_source.get_all_layer_names():
            self._metadata[layer_name] = {
                "name": layer_name,
                "schema": None,
                "feature_count": None,
                "extent": None,
                "geom_type": None,
                "crs_code": None,
            }

    def check_valid(self) -> bool:
        """
        The check_valid function checks if the metadata is valid.
        It returns True if it is, and False otherwise.

        Args:
            self: Refer to the object itself

        Returns:
            True if the metadata is valid and false otherwise

        Doc Author:
            Trelent
        """
        try:
            self._set_metadata()
            return True
        except Exception as e:
            LOGGER.error(e)
            return False

    def get_metadata_attribute(self, attribute: str, layer_name: str = None) -> Any:
        """get data for attribute in metadata
        Args:
            attribute (str): name of attribute you want to access
            layer_name (str, optional): name of layer if more than one layer exists. Defaults to None.

        Raises:
            Exception: "file contains more than one layer, provide name of layer"
            Exception: "file has no layer called <layer_name>"

        Returns:
            Any: value of the attribute requested.
        """

        def _return_attr(_layer_name: str, _attribute: str) -> Any:
            if self._metadata[_layer_name][_attribute] is None:
                self._metadata[_layer_name][_attribute] = self._get_action(
                    _layer_name, _attribute
                )()
            return self._metadata[_layer_name][_attribute]

        if self.get_layer_count() > 1 and layer_name is None:
            raise Exception("file contains more than one layer, provide name of layer")
        elif self.get_layer_count() == 1:
            layer_name = next(iter(self._metadata))
            return _return_attr(layer_name, attribute)
        elif layer_name is not None:
            if layer_name in [x['name'] for x in self.get_layers()]:
                return _return_attr(layer_name, attribute)
            else:
                raise Exception(f"file has no layer called {layer_name}")

    def _get_action(self, layer_name: str, action: str) -> Callable:
        """
        The _get_action function is a helper function that returns the appropriate action for a given layer.
        The actions are: schema, feature_count, extent, geom_type and crs_code.

        Args:
            self: Refer to the object of the class
            layer_name:str: Specify the layer that we want to perform an action on
            action:str: Specify which action to perform on the layer

        Returns:
            A callable function
        """
        layer = self._data_source.get_layer_by_name(layer_name)
        actions = {
            "schema": layer.get_schema,
            "feature_count": layer.get_feature_count,
            "extent": layer.get_extent,
            "geom_type": layer.get_geom_type,
            "crs_code": layer.get_crs_code,
        }
        return actions[action]
