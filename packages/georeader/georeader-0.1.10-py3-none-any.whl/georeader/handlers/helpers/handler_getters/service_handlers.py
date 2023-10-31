from georeader.handlers.wfs_handler import WFSHandler
from georeader.handlers.esri_rest_handler import EsriRestHandler

service_handlers = {
    "wfs": WFSHandler,
    "esri_rest": EsriRestHandler,
}