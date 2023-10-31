import logging
from georeader.handlers.general_handler import GeneralHandler


LOGGER = logging.getLogger("__name__")


class GeoPackageHandler(GeneralHandler):

    handler_type = "GeoPackage"
    source_type = "file"

    def __init__(self, file_name):
        self.GDAL_drivers = ["GPKG"]
        super(GeoPackageHandler, self).__init__(
            source=file_name,
            gdal_drivers=self.GDAL_drivers,
        )
        if self.file_extension != "gpkg":
            raise ValueError(f"{file_name} is not a gpkg file type")

        LOGGER.debug("initializing GeoPackageHandler")
        LOGGER.debug(vars(self))
