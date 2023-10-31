from unittest import TestCase
from georeader.reader import GeoReader
from georeader.handlers.layer_handler import LayerHandler
import geopandas as gpd
from pathlib import Path
import georeader.logic.ogr_helpers as ogr_helpers
import os
import shutil
import time

root_dir = Path(os.path.abspath(__file__)).parent.parent

class TestGeoreader_SHAPEFILE(TestCase):

    @classmethod
    def setUpClass(self):
        test_files_dir = "C:/Users/Nathan/code/python_apps/georeader/georeader/tests/data/"
        polygon_file = os.path.join(test_files_dir, 'polygon.json')
        self.shapefile_folder = os.path.join(test_files_dir, 'temp_files/test_shapefiles')
        os.mkdir(self.shapefile_folder)
        polygon_shapefile = os.path.join(self.shapefile_folder, 'polygon.shp')
        ogr_helpers.convert_multiple_files_to_file(
            input_files=[polygon_file],
            input_type="GEOJSON",
            output_file=polygon_shapefile,
            output_file_type="ESRI Shapefile",
        )
        self.polygon_shapefile = polygon_shapefile
        print('file should be made')

    @classmethod
    def tearDownClass(self) -> None:
        print('tear Down')
        if self.shapefile_folder is not None and os.path.exists(self.shapefile_folder):
            shutil.rmtree(self.shapefile_folder)

    def test_data_type(self):
        try:
            geo_reader_1 = GeoReader(self.polygon_shapefile)
            self.assertEqual(geo_reader_1.data_type["name"], "shp")
        finally:
            geo_reader_1.handler.destroy()

    def test_list_layers(self):
        try:
            geo_reader_1 = GeoReader(self.polygon_shapefile)
            layers = geo_reader_1.list_layers()
            self.assertListEqual(layers, ["polygon"])
        finally:
            geo_reader_1.handler.destroy()

    def test_get_schema(self):
        try:
            geo_reader_1 = GeoReader(self.polygon_shapefile)
            layer = geo_reader_1.get_layer(geo_reader_1.list_layers()[0])
            schema_1 = layer.get_schema()
            self.assertIsInstance(schema_1, list)
            true_schema = ['col1']
            self.assertListEqual(schema_1, true_schema)
        finally:
            geo_reader_1.handler.destroy()

    def test_get_dataframe(self):
        try:
            geo_reader_1 = GeoReader(self.polygon_shapefile)
            layer = geo_reader_1.layers[0]
            df = layer.get_dataframe()
            self.assertIsInstance(df, gpd.GeoDataFrame)
        finally:
            geo_reader_1.handler.destroy()

    def test_get_feature_count(self):
        geo_reader_1 = GeoReader(self.polygon_shapefile)
        layer = geo_reader_1.get_layer("UK_Historical_Earthquakes")
        count = layer.get_feature_count()
        self.assertEqual(count, 471)
