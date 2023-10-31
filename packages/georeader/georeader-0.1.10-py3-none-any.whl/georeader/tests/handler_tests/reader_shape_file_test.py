from unittest import TestCase
from georeader.reader import GeoReader
from georeader.handlers.layer_handler import LayerHandler
import geopandas as gpd
from pathlib import Path
import os

root_dir = Path(os.path.abspath(__file__)).parent.parent

gpkg_file_1 = str(
    Path.joinpath(
        root_dir, "test_files/UK_Historical_Earthquakes/UK_Historical_Earthquakes.shp"
    )
)


class TestGeoreader_GPKG(TestCase):
    def test_data_type(self):
        geo_reader_1 = GeoReader(gpkg_file_1)
        self.assertEqual(geo_reader_1.data_type["name"], "shp")

    def test_list_layers(self):
        geo_reader_1 = GeoReader(gpkg_file_1)
        layers = geo_reader_1.list_layers()
        self.assertListEqual(layers, ["UK_Historical_Earthquakes"])

    def test_layer_count(self):
        geo_reader_1 = GeoReader(gpkg_file_1)
        self.assertEqual(len(geo_reader_1.list_layers()), 1)

    def test_get_layer(self):
        geo_reader_1 = GeoReader(gpkg_file_1)
        layer_1 = geo_reader_1.get_layer("UK_Historical_Earthquakes")
        self.assertIsInstance(layer_1, LayerHandler)
        self.assertEqual(layer_1.get_layer_name(), "UK_Historical_Earthquakes")

    def test_get_schema(self):
        geo_reader_1 = GeoReader(gpkg_file_1)
        layer_1 = geo_reader_1.get_layer("UK_Historical_Earthquakes")
        layer_2 = geo_reader_1.get_layer("UK_Modern_Earthquakes")
        schema_1 = layer_1.get_schema()
        self.assertIsInstance(schema_1, list)
        true_schema = [
            "OBJECTID_1",
            "OBJECTID",
            "DY_MO_YEAR",
            "YEAR",
            "HRMN",
            "SECS",
            "LAT",
            "LON",
            "EAST",
            "NORTH",
            "DEP",
            "ML",
            "MGMC",
            "MAG",
            "INT",
            "LOCALITY",
            "COMMENTS",
        ]
        self.assertListEqual(schema_1, true_schema)

    def test_get_feature_count(self):
        geo_reader_1 = GeoReader(gpkg_file_1)
        layer = geo_reader_1.get_layer("UK_Historical_Earthquakes")
        count = layer.get_feature_count()
        self.assertEqual(count, 471)

    def test_get_dataframe(self):
        geo_reader_1 = GeoReader(gpkg_file_1)
        layer = geo_reader_1.layers[0]
        df = layer.get_dataframe()
        self.assertIsInstance(df, gpd.GeoDataFrame)
