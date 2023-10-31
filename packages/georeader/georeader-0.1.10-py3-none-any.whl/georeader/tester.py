from georeader.reader import GeoReader
from osgeo import ogr, gdal, osr
from logic.ogr.data_source import OGR_DataSource
from georeader.handlers.open_file_gdb_handler import OpenFileGDB
import atexit

wfs_url_1 = "http://www.maps.north-ayrshire.gov.uk/arcgis/services/AGOL/Spatial_Hub/MapServer/WFSServer"
wfs_url_2 = "http://inspire.dundeecity.gov.uk/geoserver/inspire/wfs"
wfs_url_3 = "http://172.20.137.132:8080/geoserver/wfs?authkey="
wfs_url_4 = "https://data.angus.gov.uk/geoserver/services/ows?request=getcapabilities&service=wfs"
wfs_url_5 = "http://172.20.137.132:8080/geoserver/sh_commcnc/wfs?service=wfs&authkey=b85aa063-d598-4582-8e45-e7e6048718fc"
wfs_url_6 = "https://geo.spatialhub.scot/geoserver/sh_commcnc/wfs?service=wfs&authkey=b85aa063-d598-4582-8e45-e7e6048718fc"
wfs_url_7 = "https://geo.spatialhub.scot/geoserver/wfs?service=wfs&authkey=b85aa063-d598-4582-8e45-e7e6048718fc"

esri_feature_server_layer = "https://services1.arcgis.com/MfbPb778y5QTu2Wv/ArcGIS/rest/services/CNP_SDAs_2010_HC/FeatureServer/0"
esri_feature_server = "https://services1.arcgis.com/MfbPb778y5QTu2Wv/ArcGIS/rest/services/CNP_SDAs_2010_HC/FeatureServer"
esri_mapserver = "https://edinburghcouncilmaps.info/arcgis/rest/services/CouncilAssets/MiscAssets/MapServer/"
esri_mapserver_layer = "https://edinburghcouncilmaps.info/arcgis/rest/services/CouncilAssets/MiscAssets/MapServer/8"
esri_mapserver_group_layer = "https://edinburghcouncilmaps.info/arcgis/rest/services/CouncilAssets/MiscAssets/MapServer/9"
esri_url_3 = 'https://services6.arcgis.com/1nr1FSi7qoFduqRA/ArcGIS/rest/services/FV_OSG_Postcode_v4_postcode_population_dissolve/FeatureServer/0'
esri_url_4 = 'https://edinburghcouncilmaps.info/arcgis/rest/services/CouncilAssets/ConfirmAssets2/MapServer/1'
esri_service_layer = "https://services1.arcgis.com/MfbPb778y5QTu2Wv/ArcGIS/rest/services/"

esri_rest_service = "https://services1.arcgis.com/MfbPb778y5QTu2Wv/ArcGIS/rest/services/12_03_19_SheilaMckandie/FeatureServer"
gml_1 = "C:/Users/Nathan/code/RESOURCES/example_spatial_files/gml/community_council_boundaries_IS.gml"

esri_rest_base = "https://edinburghcouncilmaps.info/arcgis/rest/services/"
esri_rest_base_2 = "https://services6.arcgis.com/1nr1FSi7qoFduqRA/ArcGIS/rest/services"
esri_rest_raster_layer = "https://edinburghcouncilmaps.info/arcgis/rest/services/AerialPhotography/AerialPhotos1996/MapServer/0"

zip_shape_1 = "C:/Users/Nathan/code/RESOURCES/example_spatial_files/shape/community_council_boundaries.zip"
zip_shape_2 = "C:/Users/Nathan/code/RESOURCES/example_spatial_files/shape/cycling_network.zip"

gpkg_1 = "C:/Users/Nathan/code/RESOURCES/example_spatial_files/geopackage/multi_polling_places.gpkg"


t = "C:/Users/Nathan/code/python_apps/georeader/georeader/tests/data/multi_polygon.json"
f = "https://geo.spatialhub.scot/geoserver/sh_stfnt/wfs?service=wfs&authkey=a68caf6d-7465-408a-a39c-45ace14eecda"
temp_dir = "C:/Users/Nathan/code/python_apps/georeader/georeader/tests/data/temp_files"

plnapp = "https://geo.spatialhub.scot/geoserver/sh_plnapp_premium/wfs?service=WFS&authkey=80268605-54a2-45d7-906a-f09fee88a86b"
esri_test_url_1 = "https://maps.renfrewshire.gov.uk/arcgis/rest/services/Contentmaps/LDP_ADOPTED_2021/FeatureServer"
# from georeader.logic.converters import Converters

# out_file = temp_dir + "/multi_polygon.shp"
# Converters.convert_geojson_to_shapefile(t, out_file)#
tester = "C:/Users/Nathan/code/python_apps/service_downloader/resources/aqma_1/aqma.shp"

edinburgh_esri_layer = "https://edinburghcouncilmaps.info/arcgis/rest/services/"
edinburgh_esri_layer_2 = "https://edinburghcouncilmaps.info/arcgis/rest/services/AdminBoundaries/MiscBoundaries/MapServer"
edinburgh_esri_layer_3 = "https://edinburghcouncilmaps.info/arcgis/rest/services/AdminBoundaries/MiscBoundaries/MapServer/0"

north_ayrshire = "https://www.maps.north-ayrshire.gov.uk/arcgis/services/AGOL/Spatial_Hub/MapServer/WFSServer"
if __name__ == "__main__":
    import timeit
    starttime = timeit.default_timer()
    print("The start time is :", starttime)
    # _url = "https://edinburghcouncilmaps.info/arcgis/rest/services/Misc/INSPIRE/MapServer/41/query?where=0%3D0&text=&objectIds=&time=&timeRelation=esriTimeRelationOverlaps&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=site_code%2Csite_name&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&havingClause=&returnIdsOnly=false&returnCountOnly=false&orderByFields=OBJECTID&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=10&returnExtentOnly=false&sqlFormat=none&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=pjson"
    # new_test = "https://edinburghcouncilmaps.info/arcgis/rest/services/Misc/INSPIRE/MapServer/41/query?f=json&objectIds=2932683,2932684,2932685,2932686,2932687,2932688,2932689,2932690,2932691,2932692,2932693,2932694,2932695,2932696,2932697,2932698,2932699,2932700,2932701,2932702,2932703,2932704,2932705,2932706,2932707,2932708,2932709,2932710,2932711,2932712,2932713,2932714,2932715,2932716,2932717,2932718,2932719,2932720,2932721,2932722,2932723,2932724,2932725,2932726,2932727,2932728,2932729,2932730,2932731,2932732,2932733,2932734,2932735,2932736,2932737,2932738,2932739,2932740,2932741,2932742,2932743,2932744,2932745,2932746,2932747,2932748,2932749,2932750,2932751,2932752,2932753,2932754,2932755,2932756,2932757,2932758,2932759,2932760,2932761,2932762,2932763,2932764,2932765,2932766,2932767,2932768,2932769,2932770,2932771,2932772,2932773,2932774,2932775,2932776,2932777,2932778,2932779,2932780,2932781,2932782&inSR=27700&outSR=27700&returnGeometry=true&outFields=*&returnM=false&returnZ=false&geometryPrecision=0"
    # geojson_verison = "https://edinburghcouncilmaps.info/arcgis/rest/services/Misc/INSPIRE/MapServer/41/query?f=geojson&objectIds=2932683,2932684,2932685,2932686,2932687,2932688,2932689,2932690,2932691,2932692,2932693,2932694,2932695,2932696,2932697,2932698,2932699,2932700,2932701,2932702,2932703,2932704,2932705,2932706,2932707,2932708,2932709,2932710,2932711,2932712,2932713,2932714,2932715,2932716,2932717,2932718,2932719,2932720,2932721,2932722,2932723,2932724,2932725,2932726,2932727,2932728,2932729,2932730,2932731,2932732,2932733,2932734,2932735,2932736,2932737,2932738,2932739,2932740,2932741,2932742,2932743,2932744,2932745,2932746,2932747,2932748,2932749,2932750,2932751,2932752,2932753,2932754,2932755,2932756,2932757,2932758,2932759,2932760,2932761,2932762,2932763,2932764,2932765,2932766,2932767,2932768,2932769,2932770,2932771,2932772,2932773,2932774,2932775,2932776,2932777,2932778,2932779,2932780,2932781,2932782&inSR=27700&outSR=27700&returnGeometry=true&outFields=*&returnM=false&returnZ=false&geometryPrecision=0"
    # file_geojson = "C:/Users/Nathan/Downloads/broken_json.json"
    # driver = ogr.GetDriverByName('ESRIJSON')
    # driver.SetMetadataItem("FEATURE_SERVER_PAGING", "YES", None)
    # datasource = driver.Open(f"ESRIJSON:{new_test}")
    # layer = datasource.GetLayer()
    # layer_new = datasource.ExecuteSQL('SELECT DISTINCT OBJECTID FROM ESRIJSON')
    # print("The time difference is :", timeit.default_timer() - starttime)
    # feature = layer.GetFeature(2)
    # print(feature)

    # spatialRef = osr.SpatialReference()
    # spatialRef.ImportFromEPSG(4326)
    #
    # bngRef = osr.SpatialReference()
    # bngRef.ImportFromEPSG(27700)
    # area_of_use = bngRef.GetAreaOfUse()
    # #
    # # # transform = osr.CoordinateTransformation(bngRef, spatialRef)
    # transform = osr.CoordinateTransformation(spatialRef, bngRef)
    # #
    # # lcorner = ogr.Geometry(ogr.wkbPoint)
    # # ucorner = ogr.Geometry(ogr.wkbPoint)
    # corner1 = ogr.Geometry(ogr.wkbPoint)
    # corner2 = ogr.Geometry(ogr.wkbPoint)
    # corner1.AddPoint(area_of_use.north_lat_degree, area_of_use.west_lon_degree)
    # corner2.AddPoint(area_of_use.south_lat_degree, area_of_use.east_lon_degree)
    #
    # # lcorner.AddPoint(186835.92830422127735801,615412.45445594552438706)
    # # ucorner.AddPoint(242827.57836227785446681,670211.85329036845359951)
    # # lcorner.AddPoint(55.50302371, -5.35568245)
    # # ucorner.AddPoint(55.78263531, -4.52907660)
    # # point.AddPoint(2.01, 61.01)
    # # point.AssignSpatialReference(spatialRef)
    # print(lcorner.ExportToWkt())
    # print(ucorner.ExportToWkt())
    #
    # corner1.Transform(transform)
    # corner2.Transform(transform)

    # print(corner1.ExportToJson())
    # print(corner2.ExportToJson())
    # driver = ogr.GetDriverByName('WFS')
    # datasource = driver.Open('WFS:https://www.maps.north-ayrshire.gov.uk/arcgis/services/AGOL/Spatial_Hub/MapServer/WFSServer?version=2.0.0&request=getFeature&typename=AGOL_Spatial_Hub%3ACycle_Routes&service=wfs&SRSNAME=urn%3Aogc%3Adef%3Acrs%3AEPSG%3A%3A27700&bbox=22055.7101729493%2C1256558.4455361185%2C688806.0073395604%2C-8908.368284370663%2Curn%3Aogc%3Adef%3Acrs%3AEPSG%3A%3A27700&count=30')
    # layer = datasource.GetLayer()
    #
    georeader = GeoReader("https://edinburghcouncilmaps.info/arcgis/rest/services")
    layer_list = georeader.list_layers()
    print(layer_list)
    layers = georeader.get_layers()
    layer_name = layers[2].layer_or_file_name
    layer = georeader.get_layer(layer_name)
    print(layer.get_layer_name())
    print(layer.get_schema())
    print(layer.get_feature_count())
    print(layer.get_crs_code())
    print(layer.get_dataframe())
    print(layer.get_extent())
    #
    # db_name = "Test"
    # db_user = "postgres"
    # db_pass = "Cd73a83f4b"
    # db_host = "localhost"
    # #
    # connection_str = (
    #     f"PG:dbname='{db_name}' user='{db_user}' password='{db_pass}' host='{db_host}'"
    # )
    # table_name = "test_table"
    # print(table_name)
    # schema = "public"
    # crs = 27700
    # overwrite = True
    # #
    # layer.write_to_postgis_db(
    #     table_name=table_name,
    #     schema=schema,
    #     connection_str=connection_str,
    #     crs=27700,
    #     overwrite=True,
    #     force_type=0,
    # )

    # for layer_name in georeader.list_layers():
    #     print("-----------------------------------")
    #     layer = georeader.get_layer(layer_name)
    #     print(layer.get_layer_name())
    #     print(layer.get_schema())
    #     print(layer.get_feature_count())
    #     print(layer.get_crs_code())
    #     print(layer.get_dataframe())
    #     print(layer.get_extent())
    #
    #     db_name = "Test"
    #     db_user = "postgres"
    #     db_pass = "Cd73a83f4b"
    #     db_host = "localhost"
    #
    #     connection_str = f"PG:dbname='{db_name}' user='{db_user}' password='{db_pass}' host='{db_host}'"
    #     table_name = layer_name
    #     print(table_name)
    #     schema = "public"
    #     crs = 27700
    #     overwrite = True
    #
    #     layer.write_to_postgis_db(
    #         table_name=table_name,
    #         schema=schema,
    #         connection_str=connection_str,
    #         crs=27700,
    #         overwrite=True,
    #         force_type=0
    #     )

    print("The time difference is :", timeit.default_timer() - starttime)
