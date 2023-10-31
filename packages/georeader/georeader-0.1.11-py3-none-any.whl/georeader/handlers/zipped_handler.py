import os
import sys
import py7zr
import logging
from georeader.logic.main_helpers import get_file_ext
from georeader.logic.error_exceptions import NotValid, NoSupportedFormatsFound
from georeader.handlers.base_handler import BaseHandler
from georeader.handlers.helpers.directory_helper import DirectoryHelper
from georeader.handlers.helpers.handler_getters.file_handlers import file_handlers
from geopandas import GeoDataFrame

from zipfile import ZipFile

LOGGER = logging.getLogger("__name__")


class ZippedHandler(BaseHandler, DirectoryHelper):

    handler_type = "Zip"

    def __init__(self, file_name, zip_type=None):
        super().__init__(tmp_dir=None)
        self.create_working_dir()
        if os.path.exists(file_name):
            self.file_name = file_name
        else:
            raise ValueError(f"{file_name} path does not exist")
        if zip_type is None:
            self.zip_type = get_file_ext(file_name)
        else:
            self.zip_type = zip_type
        self.file_type = None
        self.extracted_path = None
        self.handler = None
        self.handlers = {}
        if not self.check_valid():
            raise NotValid(
                self.check_valid,
                f"{file_name} does not appear to be a valid {self.zip_type} File",
            )
        self.files = self._set_files()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.delete_working_dir()

    @staticmethod
    def _get_handlers():
        handlers = file_handlers
        handlers["zip"] = ZippedHandler
        handlers["7zip"] = ZippedHandler
        return handlers

    def get_dataframe(self, layer_name=None) -> GeoDataFrame:
        return self.get_action("get_dataframe", layer_name)

    def get_all_dataframes(self) -> list:
        dataframes = []
        for layer in self.get_layers():
            dataframes.append(self.get_dataframe(layer))
        return dataframes

    def get_schema(self, layer_name=None) -> list:
        return self.get_action("get_schema", layer_name)

    def get_feature_count(self, layer_name=None):
        return self.get_action("get_feature_count", layer_name)

    def get_extent(self, layer_name=None):
        return self.get_action("get_extent", layer_name)

    def get_crs_code(self, layer_name=None):
        return self.get_action("get_crs_code", layer_name)

    def get_geom_type(self, layer_name=None):
        return self.get_action("get_geom_type", layer_name)

    def get_action(self, action, layer_name=None):
        class_function = getattr(self.handler, action)
        layer_count = self.get_layer_count()
        if layer_count > 1 and layer_name is None:
            raise Exception(
                "file_name must be provided if zip file contains multiple layers"
            )
        elif layer_count == 1:
            file_name = next(iter(self.handlers.keys()))
            return class_function(self.handlers[file_name])
        else:
            file_name = self._get_containing_file_of_layer(layer_name)
            if file_name is not None:
                return class_function(self.handlers[file_name])
            else:
                raise Exception(f"file: {layer_name} does not exist.")

    def get_layers(self) -> list:
        layers = []
        for layer_list in self.files.values():
            layers = [*layers, *layer_list]
        return layers

    def get_layer_count(self) -> int:
        return len(self.get_layers())

    def list_files_in_zip(self):
        zipped = self._get_zip_object()
        if self.zip_type in ["zip", "kmz"] and zipped is not None:
            file_list = zipped.namelist()
        elif self.zip_type == "7z":
            file_list = zipped.getnames()
        else:
            return []
        zipped.close()
        return file_list

    def _get_zip_object(self):
        if self.zip_type in ["zip", "kmz"]:
            return ZipFile(self.file_name)
        elif self.zip_type == "7z":
            return py7zr.SevenZipFile(self.file_name)
        else:
            return None

    def _set_files(self):
        data_dict = {}
        for file_name, handler in self.handlers.items():
            data_dict[file_name] = handler.get_layers()
        return data_dict

    def _get_containing_file_of_layer(self, layer_name) -> str:
        for file_name, layers in self.files.items():
            if layer_name in layers:
                return file_name

    def _set_handlers(self):
        inner_data_type = self.file_type.split(":")[1]
        if inner_data_type in self._get_handlers().keys():
            self.handler = self._get_handlers()[inner_data_type]
        else:
            raise Exception(
                f"cannot get handler, allowed zipped datasets are: {','.join(self._get_handlers().keys())}"
            )
        if self.extracted_path is None:
            self.extract_files()
        for file_path in self.get_file_paths():
            file_name = os.path.basename(file_path)
            self.handlers[file_name] = self.handler(file_path)

    def _check_file_types_within(self):
        file_types = {}
        for file in self.list_files_in_zip():
            file_extension = get_file_ext(file)
            if file_extension is not None:
                if file_extension in file_types.keys():
                    file_types[file_extension] += 1
                else:
                    file_types[file_extension] = 1
        for v_type in self._get_handlers().keys():
            if v_type in file_types.keys():
                self.file_type = f"{self.zip_type}:{v_type}"
                self._set_handlers()
                break

    def get_file_paths(self) -> list:
        if os.path.exists(self.extracted_path):
            files: list = []
            for file_path in self.get_nested_file_names(self.extracted_path):
                if get_file_ext(file_path) == self.file_type.split(":")[1]:
                    files.append(file_path)
            return files
        else:
            raise Exception(f"Error: no folder called {self.extracted_path}")

    def get_nested_file_names(self, _path, file_paths=None) -> list:
        file_paths: list = file_paths if file_paths is not None else []
        for item in os.listdir(_path):
            n_path = os.path.join(_path, item)
            if os.path.isdir(n_path):
                if get_file_ext(n_path) == self.file_type.split(":")[1]:
                    file_paths.append(n_path)
                self.get_nested_file_names(n_path, file_paths)
            else:
                file_paths.append(n_path)
        return file_paths

    def get_extracted_file_paths(self) -> list:
        files = []
        for file in self.get_file_names():
            path = os.path.join(self.extracted_path, file)
            files.append(path)
        return files

    def extract_files(self, retry=True) -> bool:
        if self.extracted_path is not None:
            return True
        try:
            extracted_folder_path = os.path.join(self.working_dir, "extracted_files")
            os.mkdir(extracted_folder_path)
            zipped_file = self._get_zip_object()
            zipped_file.extractall(extracted_folder_path)
            zipped_file.close()

            folder_name = os.path.splitext(os.path.basename(self.file_name))[0]
            possible_folder_path = os.path.join(
                str(extracted_folder_path), str(folder_name)
            )
            if os.path.isdir(possible_folder_path):
                extracted_folder_path = possible_folder_path
            self.extracted_path = extracted_folder_path
        except Exception as e:
            raise Exception(f"failed to extract files, error: {e}")
        return True

    def check_valid(self):
        self._check_file_types_within()
        if self.zip_type is None:
            return False
        if self.file_type is None:
            raise NoSupportedFormatsFound(
                self._check_file_types_within,
                f"No supported file formats found in {self.file_name}",
            )
        return True
