import logging
import geopandas as gpd
from georeader.handlers.general_handler import GeneralHandler
from georeader.handlers.helpers.handler_decorators import pre_action_check
from typing import List

LOGGER = logging.getLogger("__name__")


class KMLHandler(GeneralHandler):

    handler_type = "KML"
    source_type = "file"

    def __init__(self, file_name):
        self.GDAL_drivers = ["LIBKML"]
        super(KMLHandler, self).__init__(
            source=file_name, gdal_drivers=self.GDAL_drivers
        )
        if self.file_extension != "kml":
            raise ValueError(f"{file_name} is not a kml file type")
        LOGGER.debug("initializing KMLHandler")
        LOGGER.debug(vars(self))

    @pre_action_check
    def get_dataframe(self, layer_name: str = None) -> gpd.geodataframe:
        if layer_name is None:
            layer_name = list(self._metadata.keys())[0]
        layer = self._data_source.get_layer_by_name(layer_name)
        return layer.get_dataframe(schema=self.get_schema())

    @pre_action_check
    def get_schema(self, layer_name: str = None) -> List[str]:
        """return layer schema
        Args:
            layer_name (str, optional): name of layer if more than one layer exists. Defaults to None.
        Returns:
            List[str]: return list of attribute names.
        """
        if self._metadata[layer_name]["schema"] is not None:
            return self._metadata[layer_name]["schema"]
        else:
            self._metadata[layer_name]["schema"] = self._data_source.get_layer_by_name(
                layer_name
            ).get_schema()[11:]
            return self._metadata[layer_name]["schema"]
