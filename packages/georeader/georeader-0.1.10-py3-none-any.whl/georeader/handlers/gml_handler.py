import configparser
import logging
from georeader.handlers.general_handler import GeneralHandler

config = configparser.ConfigParser()
LOGGER = logging.getLogger("__name__")


class GMLHandler(GeneralHandler):

    handler_type = "GML"
    source_type = "file"

    def __init__(self, file_name):
        self.GDAL_drivers = ["GML"]
        super(GMLHandler, self).__init__(
            source=file_name,
            gdal_drivers=self.GDAL_drivers,
        )
        if self.file_extension not in ("xml", "gml"):
            raise ValueError(f"{file_name} is not a gml/xml file type")
        self.create_working_dir()
        LOGGER.debug("initializing GMLHandler")
        LOGGER.debug(vars(self))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.delete_working_dir()
