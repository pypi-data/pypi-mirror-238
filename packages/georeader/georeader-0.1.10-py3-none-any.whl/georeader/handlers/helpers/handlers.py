import configparser
import os
from pathlib import Path

config = configparser.ConfigParser()
file_dir = Path(os.path.dirname(os.path.abspath(__file__)))
georeader_root_dir = file_dir.parent.parent.absolute()
config_path = georeader_root_dir.joinpath('config.ini')
print(config_path)
config.read(config_path)

# valid_file_types = config['valid_types']['valid_files'].split(',')
# valid_zip_types = config['valid_types']['valid_zip'].split(',')
# valid_service_types = config['valid_types']['valid_services'].split(',')
# valid_db_types = config['valid_types']['valid_db'].split(',')

valid_file_types = ['gpkg', 'geojson', 'json', 'shp', 'gml', 'csv', 'kmz', 'gdb', 'xml']
valid_service_types = ['wfs', 'esri_rest']
valid_zip_types = ['kmz', 'zip', '7z']
valid_db_types = ['postgresql']

# valid_file_types = [
#     "gpkg": "GeoPackage"
# ]

def is_valid_type(_type: str) -> bool:
    if is_valid_db_type(_type) or\
            is_valid_zip_type(_type) or\
            is_valid_service_type(_type) or\
            is_valid_file_type(_type):
        return True

def is_valid_db_type(_type: str):
    if _type in valid_db_types:
        return True
    else:
        return False


def is_valid_service_type(_type: str):
    if _type in valid_service_types:
        return True
    else:
        return False


def is_valid_file_type(_type: str):
    if _type in valid_file_types:
        return True
    else:
        return False


def is_valid_zip_type(_type: str):
    if _type in valid_zip_types:
        return True
    else:
        return False


def get_handler_zip(_type: str):
    if is_valid_zip_type(_type):
        from georeader.handlers.helpers.handler_getters.zip_handlers import zip_handlers
        return zip_handlers[_type]
    else:
        raise ValueError(f'{_type} is not supported')


def get_handler_file(_type: str):
    if is_valid_file_type(_type):
        from georeader.handlers.helpers.handler_getters.file_handlers import file_handlers
        return file_handlers[_type]
    else:
        raise ValueError(f'{_type} is not supported')


def get_handler_service(_type: str):
    if is_valid_service_type(_type):
        from georeader.handlers.helpers.handler_getters.service_handlers import service_handlers
        return service_handlers[_type]
    else:
        raise ValueError(f'{_type} is not supported')


def get_handler_db(_type: str):
    if is_valid_db_type(_type):
        from georeader.handlers.helpers.handler_getters.db_handlers import db_handlers
        return db_handlers[_type]
    else:
        raise ValueError(f'{_type} is not supported')
