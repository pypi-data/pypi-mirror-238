from unittest import TestCase
from georeader.reader import GeoReader
from georeader.handlers.layer_handler import LayerHandler
import geopandas as gpd

wfs_url_1 = "http://172.20.137.132:8080/geoserver/wfs?authkey=b85aa063-d598-4582-8e45-e7e6048718fc"


class TestGeoreader_WFS(TestCase):
    def test_wfs_data_type(self):
        geo_reader_1 = GeoReader(wfs_url_1)
        self.assertEqual(geo_reader_1.data_type["name"], "wfs")

    def test_layer_count(self):
        geo_reader_1 = GeoReader(wfs_url_1)
        self.assertGreater(len(geo_reader_1.list_layers()), 1)

    def test_get_layer(self):
        geo_reader_1 = GeoReader(wfs_url_1)
        layers = geo_reader_1.layers
        layer = layers[0]
        self.assertIsInstance(layer, LayerHandler)

    def test_get_schema(self):
        geo_reader_1 = GeoReader(wfs_url_1)
        layer = geo_reader_1.layers[0]
        schema = layer.get_schema()
        self.assertIsInstance(schema, list)
        self.assertGreater(len(schema), 1)

    def test_get_dataframe(self):
        geo_reader_1 = GeoReader(wfs_url_1)
        layer = geo_reader_1.get_layer("sh_polpl:pub_polpl")
        df = layer.get_dataframe()
        self.assertIsInstance(df, gpd.GeoDataFrame)
