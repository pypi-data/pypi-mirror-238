import os
import logging

import pandas
import pandas as pd
import csv
import shapely
import geopandas as gpd
from pathlib import Path
from typing import Union, Any
from georeader.handlers.base_handler import BaseHandler
from georeader.logic.main_helpers import get_file_ext
from georeader.logic.error_exceptions import NotValid
from contextlib import suppress
from osgeo import ogr, gdal
import warnings

warnings.filterwarnings("ignore", "GeoSeries.notna", UserWarning)

gdal.UseExceptions()

LOGGER = logging.getLogger("csv_handler")


class CSVHandler(BaseHandler):
    """
    handler for csv files.
    """

    handler_type = "CSV"

    def __init__(self, file_name: str):
        if os.path.exists(file_name):
            self.file_name = file_name
        else:
            error = f"{file_name} path does not exist"
            LOGGER.error(error)
            raise ValueError(error)
        self.file_extension = get_file_ext(self.file_name)
        self.df = None
        self._metadata = {}
        if not self.check_valid():
            error = f"{file_name} does not appear to be a valid CSV"
            logging.error(error)
            raise NotValid(self.check_valid, error)
        LOGGER.debug("initializing CSVHandler")
        LOGGER.debug(vars(self))

    def get_file_name(self) -> str:
        """returns file name

        Returns:
            str: file name
        """
        return self.file_name

    @staticmethod
    def get_layer_count(*args, **kwargs) -> int:
        """returns layer count. layer count will always for text based files.

        Returns:
            int: number of layer (1)
        """
        return 1

    def get_layers(self) -> list:
        """return list of layers

        Returns:
            list: layer list
        """
        return [{"name": Path(self.file_name).with_suffix("").name}]

    def get_feature_count(self, *args, **kwargs) -> int:
        """returns number of features in layer

        Returns:
            int: feature count
        """
        return len(self._read_as_df())

    def convert_df_into_gdf(self, dataframe: pd.DataFrame) -> gpd.GeoDataFrame:
        """This function tries to convert a pandas dataframe into a geopandas dataframe

        Args:
            dataframe (pd.DataFrame):

        Returns:
            gpd.GeoDataFrame: geopandas dataframe possibly with no geom.
        """

        wkb_cols = self._get_wkb_col_from_df(dataframe)
        wkt_cols = self._get_wkt_col_from_df(dataframe)
        gdf = None

        if len(wkb_cols) > 0:
            geom_field = wkb_cols[0]
            gdf = gpd.GeoDataFrame(
                dataframe,
                geometry=[shapely.wkb.loads(x) for x in dataframe[geom_field]],
            )
            gdf.drop(geom_field, axis=1, inplace=True)
        elif len(wkt_cols) > 0:
            geom_field = wkt_cols[0]
            gdf = gpd.GeoDataFrame(
                dataframe,
                geometry=[shapely.wkt.loads(x) for x in dataframe[geom_field]],
            )
            gdf.drop(geom_field, axis=1, inplace=True)
        else:
            columns = dataframe.columns
            possible_point_sets = [
                ("x", "y"),
                ("lng", "lat"),
                ("longitude", "latitude"),
                ("east", "north"),
                ("easting", "northing"),
                ("eastings", "northings"),
            ]
            for point_set in possible_point_sets:
                confirmed = []
                for point_col in point_set:
                    for column in columns:
                        if column.lower() == point_col:
                            confirmed.append(column)
                        if len(confirmed) == 2:
                            gdf = gpd.GeoDataFrame(
                                dataframe,
                                geometry=gpd.points_from_xy(
                                    dataframe[confirmed[0]], dataframe[confirmed[1]]
                                ),
                            )
        if gdf is None:
            return gpd.read_file(self.file_name)
        return gdf

    def get_crs_code(self, layer_name: str = None) -> Union[str, None]:
        """return crs code

        Returns:
            (str): crs code
        """
        return self._metadata[layer_name]["crs_code"]

    def get_geom_type(self, layer_name: str = None) -> Union[str, None]:
        """returns geom type for layer
        Returns:
            str: name of geom type e.g polygon, point...
        """
        return self._metadata[layer_name]["geom_type"]

    def get_extent(self, layer_name: str = None) -> Union[tuple, None]:
        """Returns a tuple containing minx, miny, maxx, maxy values for layer.

        Returns:
            list: layer list
        """
        return self._metadata[layer_name]["extent"]

    def get_dataframe(self, *args, **kwargs) -> gpd.GeoDataFrame:
        """returns geopandas dataframe.

        Returns:
            gpd.GeoDataFrame:
        """
        gdf = self.convert_df_into_gdf(self._read_as_df())
        return gdf

    def _read_as_df(self) -> pandas.DataFrame:
        """reads csv into a pandas data frame
        Returns:
            (pandas.DataFrame)
        """
        return pd.read_csv(self.file_name, encoding="utf-8", encoding_errors="ignore")

    def get_schema(self, *args, **kwargs) -> list:
        """returns layer schema

        Raises:
            Exception: Fails to get schema.

        Returns:
            list: return list of attribute names.
        """
        dataframe = self._read_as_df()
        geom_fields_wkb = self._get_wkb_col_from_df(dataframe)
        geom_fields_wkt = self._get_wkt_col_from_df(dataframe)
        try:
            if self._metadata.get("schema") is not None:
                return self._metadata.get("schema")
            else:
                schema = list(dataframe.columns)
                for geom_field in [*geom_fields_wkb, *geom_fields_wkt]:
                    schema.remove(geom_field)
                self._metadata["schema"] = schema
                return schema
        except Exception as e:
            LOGGER.error(e)
            raise Exception(f"Failed to get schema from {self.file_name}")

    def _get_wkb_col_from_df(self, dataframe: pd.DataFrame) -> list:
        """gets wkb geometry col name from pandas dataframe if exists

        Args:
            dataframe (pd.DataFrame): pandas dataframe

        Returns:
            list: list of wkb geometry columns. ideally only one
        """
        return self._find_geom_col_if_exists(dataframe, "wkb")

    def _get_wkt_col_from_df(self, dataframe: pd.DataFrame) -> list:
        """gets wkt geometry col name from pandas dataframe if exists

        Args:
            dataframe (pd.DataFrame): pandas dataframe

        Returns:
            list: list of wkb geometry columns. ideally only one
        """
        return self._find_geom_col_if_exists(dataframe, "wkt")

    @staticmethod
    def _find_geom_col_if_exists(dataframe: pd.DataFrame, text_type: str) -> list:
        """gets geometry col of type wkb or wkt based on text_type param

        Args:
            dataframe (pd.DataFrame): pandas dataframe
            text_type (string): Can be 'wkt' or 'wkb'

        Returns:
            list: list: list of wkb geometry columns. ideally only one
        """
        first_item = dataframe.iloc[0]
        geom_fields = []
        for key in first_item.keys().values:
            value = first_item.get(key)
            with suppress(Exception):
                if text_type == "wkb":
                    geom_value = ogr.CreateGeometryFromWkb(value)
                else:
                    geom_value = ogr.CreateGeometryFromWkt(value)
                if geom_value is not None:
                    geom_fields.append(key)
        return geom_fields

    def check_valid(self) -> bool:
        """does some very basic checks to see if the file seems valid.

        Returns:
            bool: returns True if valid and False if not.
        """
        try:
            with open(self.file_name, "r") as read_obj:
                csv_reader = csv.reader(read_obj)
                layer_name = self.get_layers()[0]['name']
                df = self._read_as_df()
                gdf = self.convert_df_into_gdf(df)
                if gdf[gdf["geometry"].notnull()].shape[0] > 3:
                    extent = gdf.total_bounds
                    geom_type = gdf.geom_type[0]
                else:
                    extent = None
                    geom_type = None
                self._metadata[layer_name] = {
                    "name": layer_name,
                    "schema": list(gdf.columns),
                    "feature_count": df.shape[0],
                    "extent": extent,
                    "geom_type": geom_type,
                    "crs_code": gdf.crs,
                }
            return True
        except Exception as e:
            LOGGER.error(f"failed to read {self.file_extension}, Error:{e}")
            return False
