import logging
from georeader.handlers.general_handler import GeneralHandler

LOGGER = logging.getLogger("__name__")


class JSONHandler(GeneralHandler):

    handler_type = "GeoJSON"
    source_type = "file"

    def __init__(self, file_name: str):
        self.GDAL_drivers = ["GEOJSON", "ESRIJSON"]
        super(JSONHandler, self).__init__(
            source=file_name,
            gdal_drivers=self.GDAL_drivers
        )
        if self.file_extension not in ["geojson", "json"]:
            raise ValueError(f"{file_name} is not a json/geojson file type")
