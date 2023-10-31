import os
import logging
import shapefile
import pathlib
from georeader.logic.main_helpers import get_file_ext
from georeader.handlers.general_handler import GeneralHandler

LOGGER = logging.getLogger("__name__")


class ShapeFileHandler(GeneralHandler):

    handler_type = "shp"
    source_type = "file"

    def __init__(self, file_name: str):
        self.GDAL_drivers = ["ESRI Shapefile"]
        super(ShapeFileHandler, self).__init__(
            source=file_name,
            gdal_drivers=self.GDAL_drivers
        )
        if get_file_ext(file_name) != "shp":
            raise ValueError(f"{file_name} is not a shape file")
        LOGGER.debug("initializing GeoPackageHandler")
        LOGGER.debug(vars(self))

    def check_valid(self) -> bool:
        try:
            folder = os.path.dirname(self.source)
            file_base = os.path.basename(self.source).split(".")[0]
            for ext in [".dbf", ".shx"]:
                f_name = f"{file_base}{ext}"
                file_path = os.path.join(folder, f_name)
                if not os.path.exists(file_path):
                    if ext == ".shx":
                        dbf_file_path = str(
                            pathlib.PurePath(folder, file_base).with_suffix(".dbf")
                        )
                        shp_file = open(self.source, "rb")
                        dbf_file = open(dbf_file_path, "rb")
                        r = shapefile.Reader(shp=shp_file, dbf=dbf_file)
                        fixed_file = str(
                            pathlib.PurePath(folder, f"fixed_{file_base}").with_suffix(
                                ".shp"
                            )
                        )
                        w = shapefile.Writer(target=fixed_file, shapeType=r.shapeType)
                        w.fields = r.fields[1:]
                        for shape_rec in r.iterShapeRecords():
                            w.record(*shape_rec.record)
                            w.shape(shape_rec.shape)
                        w.close()
                        self.source = fixed_file
                    else:
                        LOGGER.error(f"Missing mandatory file {file_base}{ext}")
                        return False
            self._set_metadata()
            return True
        except Exception as e:
            LOGGER.error(f"failed to transform shp into dataframe, Error:{e}")
            return False
