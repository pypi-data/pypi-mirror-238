from abc import ABC, abstractmethod
from typing import Union
import geopandas as gpd


class BaseHandler(ABC):
    """
    Base Abstract Handler class that is inherited by all subsequent handlers to enforce functions.
    """

    @abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abstractmethod
    def get_feature_count(self, **kwargs) -> int:
        """returns number of features in layer

        Returns:
            int: feature count
        """
        pass

    @abstractmethod
    def get_dataframe(self, **kwargs) -> gpd.geodataframe:
        """returns geodataframe if possible

        Returns:
            gpd.geodataframe: geodataframe
        """
        pass

    @abstractmethod
    def get_schema(self, **kwargs) -> list:
        """returns layer schema

        Returns:
            list: layer schema
        """
        pass

    @abstractmethod
    def get_layer_count(self, **kwargs) -> int:
        """returns layer count

        Returns:
            int: layer count
        """
        pass

    @abstractmethod
    def get_layers(self, **kwargs) -> list:
        """return list of layers

        Returns:
            list: layer list
        """
        pass

    @abstractmethod
    def get_extent(self, **kwargs) -> Union[tuple, None]:
        """Returns a tuple containing minx, miny, maxx, maxy values for layer.

        Returns:
            list: layer list
        """
        pass

    @abstractmethod
    def get_crs_code(self, **kwargs) -> Union[str, None]:
        """return crs code

        Returns:
            (str): crs code
        """
        pass
