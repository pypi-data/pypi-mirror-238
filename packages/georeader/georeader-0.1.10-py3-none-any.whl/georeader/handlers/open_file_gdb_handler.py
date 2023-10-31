import logging
import sys
from georeader.handlers.general_handler import GeneralHandler

LOGGER = logging.getLogger("__name__")


class OpenFileGDB(GeneralHandler):

    handler_type = "OpenFileGDB"
    source_type = "file"

    def __init__(self, file_name: str):
        self.GDAL_drivers = ["OpenFileGDB"]
        print(file_name)
        super(OpenFileGDB, self).__init__(
            source=file_name, gdal_drivers=self.GDAL_drivers
        )
        if self.file_extension != "gdb":
            raise ValueError(f"{file_name} is not a gbd file type")
        LOGGER.debug(f"initializing {self.handler_type}")
        LOGGER.debug(vars(self))

    def check_valid(self) -> bool:
        if sys.platform.startswith("win"):
            if len(self.source) > 260:
                raise Exception("windows path length exceeds 260")
            if self.source.startswith("\\\\?\\"):
                self.source = self.source[4:]
        try:
            self._set_metadata()
            return True
        except Exception as e:
            LOGGER.error(e)
            return False
