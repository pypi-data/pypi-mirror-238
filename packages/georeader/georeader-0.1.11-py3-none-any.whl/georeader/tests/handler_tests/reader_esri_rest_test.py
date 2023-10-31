from unittest import TestCase
from georeader.reader import GeoReader
from georeader.handlers.layer_handler import LayerHandler
import geopandas as gpd

esr_rest_url_1 = "https://services3.arcgis.com/7bJVHfju2RXdGZa4/arcgis/rest/services/UK_Historical_Earthquakes/FeatureServer/0"


class TestGeoreader_EsriRest(TestCase):
    def test_data_type(self):
        geo_reader_1 = GeoReader(esr_rest_url_1)
        self.assertEqual(geo_reader_1.data_type["name"], "esri_rest")

    def test_list_layers(self):
        geo_reader_1 = GeoReader(esr_rest_url_1)
        layers = geo_reader_1.list_layers()
        self.assertListEqual(layers, ["UK Historical Earthquakes"])

    def test_layer_count(self):
        geo_reader_1 = GeoReader(esr_rest_url_1)
        self.assertEqual(len(geo_reader_1.list_layers()), 1)

    def test_get_layer(self):
        geo_reader_1 = GeoReader(esr_rest_url_1)
        layer = geo_reader_1.get_layer("UK Historical Earthquakes")
        self.assertIsInstance(layer, LayerHandler)
        self.assertEqual(layer.get_layer_name(), "UK Historical Earthquakes")

    def test_get_schema(self):
        geo_reader_1 = GeoReader(esr_rest_url_1)
        layer = geo_reader_1.layers[0]
        schema = layer.get_schema()
        self.assertIsInstance(schema, list)
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
        self.assertListEqual(schema, true_schema)

    def test_get_feature_count(self):
        geo_reader_1 = GeoReader(esr_rest_url_1)
        layer = geo_reader_1.layers[0]
        count = layer.get_feature_count()
        self.assertEqual(count, 471)

    def test_get_dataframe(self):
        geo_reader_1 = GeoReader(esr_rest_url_1)
        layer = geo_reader_1.layers[0]
        df = layer.get_dataframe()
        self.assertIsInstance(df, gpd.GeoDataFrame)
