from osgeo import ogr, gdal
from georeader.logic.ogr.layer import OGR_Layer
import atexit
import os

gdal.SetConfigOption("GDAL_HTTP_UNSAFESSL", "YES")


class OGR_DataSource:
    def __init__(self, _input, _type):
        self._input = _input
        self._type = _type
        self.data_source = self._get_datasource(_input, _type)
        atexit.register(self._exit_clean_up)

    @staticmethod
    def _get_datasource(_input: str, _type: str):
        """
        The _get_datasource function takes a string as input and returns an OGR datasource object.
        The function is used to abstract the logic of opening different types of data sources, such as WFS, ESRIJSON, etc.


        Args:
            _input:str: Specify the input data source
            _type:str: Specify the type of datasource

        Returns:
            A datasource object
        """
        driver = ogr.GetDriverByName(_type)
        if _type in ["WFS", "ESRIJSON"]:
            return driver.Open(f"{_type}:{_input}")
        return driver.Open(_input)

    def _exit_clean_up(self):
        """
        The _exit_clean_up function is called when the program exits. It closes the data source and
        destroys all of its children.

        Args:
            self: Refer to the object itself

        Returns:
            None
        """
        if self.data_source is not None:
            self.destroy()

    def data_source_exist(self):
        """
        The data_source_exist function checks to see if the data_source attribute of the class is None. If it is, then
        the function returns False. Otherwise, it returns True.

        Args:
            self: Access variables that belongs to the class

        Returns:
            A boolean value, true or false
        """
        if self.data_source is None:
            return False
        else:
            return True

    def destroy(self):
        """
        The destroy function is used to destroy the data source.

        Args:
            self: Access the attributes and methods of the class in python

        Returns:
            None
        """
        self.data_source.Destroy()

    def restore(self):
        """
        The restore function restores the data source to its original state.

        Args:
            self: Access the attributes and methods of the class in python

        Returns:
            The data source
        """
        self.data_source = self._get_datasource(self._input, self._type)

    def get_layer_count(self):
        """
        The get_layer_count function returns the number of layers in a data source.

        Args:
            self: Access the attributes and methods of the class in python

        Returns:
            The number of layers in a dataset
        """
        return self.data_source.GetLayerCount()

    def get_all_layer_names(self):
        """
        The get_all_layer_names function returns a list of all the layer names in the data source.

        Args:
            self: Access the object's attributes and methods

        Returns:
            A list of the names of all layers in a shapefile
        """
        return [layer.GetName() for layer in self.data_source]

    def get_layer_by_name(self, name):
        return OGR_Layer(self.data_source.GetLayerByName(name), self._type)
