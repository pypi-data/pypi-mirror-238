from georeader.handlers.csv_handler import CSVHandler
from georeader.handlers.gml_handler import GMLHandler
from georeader.handlers.gpkg_handler import GeoPackageHandler
from georeader.handlers.shape_file_handler import ShapeFileHandler
from georeader.handlers.kml_handler import KMLHandler
from georeader.handlers.json_handler import JSONHandler
from georeader.handlers.open_file_gdb_handler import OpenFileGDB

file_handlers = {
    "csv": CSVHandler,
    "gml": GMLHandler,
    "xml": GMLHandler,
    "gpkg": GeoPackageHandler,
    "shp": ShapeFileHandler,
    "kml": KMLHandler,
    "json": JSONHandler,
    "geojson": JSONHandler,
    "gdb": OpenFileGDB,
}
