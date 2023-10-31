from osgeo import ogr, osr, gdal
import os
import configparser
import geopandas as gpd
import requests
import logging
from shapely.wkb import loads

# Speeds up querying WFS capabilities for services with alot of layers
gdal.SetConfigOption('OGR_WFS_LOAD_MULTIPLE_LAYER_DEFN', 'NO')
# Set config for paging. Works on WFS 2.0 services and WFS 1.0 and 1.1 with some other services.
gdal.SetConfigOption('OGR_WFS_PAGING_ALLOWED', 'YES')
gdal.SetConfigOption('OGR_WFS_PAGE_SIZE', '10000')

config = configparser.ConfigParser()

LOGGER = logging.getLogger("__name__")


def linestring_to_multi_linestring(line_string: ogr.Geometry):
    """
    The linestring_to_multi_linestring function takes a line string and returns a multi-linestring.

    Args:
        line_string:ogr.Geometry: Pass a linestring to the function

    Returns:
        A multi_linestring geometry
    """
    multi_linestring = ogr.Geometry(ogr.wkbMultiLineString)
    multi_linestring.AddGeometry(line_string)
    return multi_linestring


def polygon_to_multi_polygon(polygon: ogr.Geometry):
    """
    The polygon_to_multi_polygon function takes a polygon and returns a multi_polygon.

    Args:
        polygon:ogr.Geometry: Set the polygon that is converted to a multi-polygon

    Returns:
        A multipolygon geometry
    """
    multi_polygon = ogr.Geometry(ogr.wkbMultiPolygon)
    multi_polygon.AddGeometry(polygon)
    return multi_polygon


def point_to_multi_point(point: ogr.Geometry):
    """
    The point_to_multi_point function takes a point and return a multi_point

    Args:
        point:ogr.Geometry: Create a new ogr

    Returns:
        A multipoint geometry from a point geometry
    """
    multi_point = ogr.Geometry(ogr.wkbMultiPolygon)
    multi_point.AddGeometry(point)
    return multi_point


def single_geom_to_multi_geom(geometry: ogr.Geometry):
    """
    The single_geom_to_multi_geom function converts a single geometry to a multi-geometry.
    The function takes an ogr.Geometry object as input and returns the same type of geometry, but with
    a different GeometryType (e.g., from Point to MultiPoint). The function is intended for use in converting
    single geometries into multi-geometries.

    Args:
        geometry:ogr.Geometry: Specify the geometry to be converted

    Returns:
        A geometry that is a multipart version of the input geometry
    """
    if geometry.GetGeometryType() == 1:
        return point_to_multi_point(geometry)
    elif geometry.GetGeometryType() == 2:
        return linestring_to_multi_linestring(geometry)
    elif geometry.GetGeometryType() == 3:
        return polygon_to_multi_polygon(geometry)
    else:
        return geometry



def convert_multiple_files_to_file(
    input_files: list,
    input_type: str,
    output_file: str,
    output_file_type: str,
    input_sample_file: str = None,
):
    """Convert multiple input files of the same type to an different format

    Args:
        input_files (list): [description]
        input_type (str): type of input:
        input_sample_file (str): [description]
        output_file (str): [description]
        output_file_type (str): [description]
    """
    try:
        # Get the input Layer
        in_driver = ogr.GetDriverByName(input_type)
        if input_sample_file is None:
            in_data_source = in_driver.Open(input_files[0], 0)
            in_layer = in_data_source.GetLayer()
        else:
            in_data_source = in_driver.Open(input_sample_file, 0)
            in_layer = in_data_source.GetLayer()

        # Create the output Layers
        outfile = os.path.join(output_file)
        out_driver = ogr.GetDriverByName(output_file_type)

        # Remove output shapefile if it already exists
        if os.path.exists(outfile):
            out_driver.DeleteDataSource(outfile)

        # Create the output shapefile
        out_data_source = out_driver.CreateDataSource(outfile)
        out_lyr_name = os.path.splitext(os.path.split(outfile)[1])[0]
        out_layer = out_data_source.CreateLayer(out_lyr_name)

        # Add input Layer Fields to the output Layer if it is the one we want
        copy_field_definitions(in_layer, out_layer)

        if input_sample_file is None and len(input_files) == 1:
            out_layer = copy_features(in_layer, out_layer)
        else:
            for file in input_files:
                in_data_source = in_driver.Open(file, 0)
                in_layer = in_data_source.GetLayer()
                out_layer = copy_features(in_layer, out_layer)
                in_data_source.Destroy()
        out_data_source.Destroy()
    except Exception as e:
        LOGGER.error(e)
        try:
            in_data_source.Destroy()
            out_data_source.Destroy()
        except NameError:
            pass


def convert_multiple_files_to_dataframe(
        input_files: list, input_type: str, input_sample_file: str = None) -> gpd.geodataframe:
    try:
        in_driver = ogr.GetDriverByName(input_type)
        if input_sample_file is None:
            in_data_source = in_driver.Open(input_files[0], 0)
            in_layer_schema = in_data_source.GetLayer()
        else:
            in_data_source = in_driver.Open(input_sample_file, 0)
            in_layer_schema = in_data_source.GetLayer()

        in_layer_def = in_layer_schema.GetLayerDefn()
        data_dict = {}
        for i in range(0, in_layer_def.GetFieldCount()):
            field_def = in_layer_def.GetFieldDefn(i)
            name = field_def.GetNameRef()
            data_dict[name] = []
        data_dict["geometry"] = []

        for file in input_files:
            in_data_source = in_driver.Open(file, 0)
            in_layer = in_data_source.GetLayer()
            in_layer_def = in_layer.GetLayerDefn()
            for in_feature in in_layer:
                for i in range(0, in_layer_def.GetFieldCount()):
                    field_def = in_layer_def.GetFieldDefn(i)
                    name = field_def.GetNameRef()
                    value = in_feature.GetField(i)
                    data_dict[name].append(value)

                geom = in_feature.GetGeometryRef()
                geom = geom.Normalize()
                geom_wkb = bytes(geom.ExportToWkb())
                shapely_geom = loads(geom_wkb)
                data_dict["geometry"].append(shapely_geom)
            in_data_source.Destroy()
        gdf = gpd.GeoDataFrame(data_dict)
        return gdf
    except Exception as e:
        LOGGER.error(f'Unable to read layer {e}')
        try:
            in_data_source.Destroy()
        except NameError:
            pass


def copy_field_definitions(in_layer, out_layer):
    in_layer_def = in_layer.GetLayerDefn()
    for i in range(0, in_layer_def.GetFieldCount()):
        field_def = in_layer_def.GetFieldDefn(i)
        out_layer.CreateField(field_def)
    return out_layer


def copy_features(in_layer, out_layer):
    out_layer_def = out_layer.GetLayerDefn()
    for in_feature in in_layer:
        out_layer.CreateFeature(in_feature)
    return out_layer


def copy_features_2(in_layer, out_layer):
    out_layer_def = out_layer.GetLayerDefn()
    for in_feature in in_layer:
        out_feature = ogr.Feature(out_layer_def)
        for i in range(0, out_layer_def.GetFieldCount()):
            field_def = out_layer_def.GetFieldDefn(i)
            out_feature.SetField(field_def.GetNameRef(), in_feature.GetField(i))
        geom = in_feature.GetGeometryRef()
        out_feature.SetGeometry(geom.Clone())
        out_layer.CreateFeature(in_feature)
    return out_layer


def get_data_from_url(url):
    response = requests.get(url)
    data = response.content.decode("utf-8")
    return data


def convert_multiple_urls_to_file(
    input_urls: list,
    input_type: str,
    input_sample_url: str,
    output_file: str,
    output_file_type: str,
):
    # define drivers
    out_driver = ogr.GetDriverByName(output_file_type)
    in_driver = ogr.GetDriverByName(input_type)

    # Remove output shapefile if it already exists
    if os.path.exists(output_file):
        out_driver.DeleteDataSource(output_file)

    # Create the output data file
    out_data_source = out_driver.CreateDataSource(output_file)
    out_lyr_name = os.path.splitext(os.path.split(output_file)[1])[0]
    out_layer = out_data_source.CreateLayer(out_lyr_name)

    # set schema of out_layer
    data = get_data_from_url(input_sample_url)
    in_data_source = in_driver.Open(data, 0)
    in_layer = in_data_source.GetLayer()
    copy_field_definitions(in_layer, out_layer)
    in_data_source.Destroy()

    for url in input_urls:
        data = get_data_from_url(url)
        in_data_source = in_driver.Open(data, 0)
        in_layer = in_data_source.GetLayer()
        copy_features(in_layer, out_layer)
        in_data_source.Destroy()
    out_data_source.Destroy()
    return output_file

# def convert_multiple_urls_to_ogr_layer(
#     input_urls: list,
#     input_type: str,
#     input_sample_url: str,
#     output_file: str,
#     output_file_type: str,
# ):
#     # define drivers
#     out_driver = ogr.GetDriverByName(output_file_type)
#     in_driver = ogr.GetDriverByName(input_type)
#
#     # Remove output shapefile if it already exists
#     if os.path.exists(output_file):
#         out_driver.DeleteDataSource(output_file)
#
#     # Create the output data file
#     out_data_source = out_driver.CreateDataSource(output_file)
#     out_lyr_name = os.path.splitext(os.path.split(output_file)[1])[0]
#     out_layer = out_data_source.CreateLayer(out_lyr_name)
#
#     # set schema of out_layer
#     data = get_data_from_url(input_sample_url)
#     in_data_source = in_driver.Open(data, 0)
#     in_layer = in_data_source.GetLayer()
#     copy_field_definitions(in_layer, out_layer)
#     in_data_source.Destroy()
#
#     for url in input_urls:
#         data = get_data_from_url(url)
#         in_data_source = in_driver.Open(data, 0)
#         in_layer = in_data_source.GetLayer()
#         copy_features(in_layer, out_layer)
#         in_data_source.Destroy()
#     out_data_source.Destroy()
#     return output_file
#
#

def convert_multiple_urls_to_dataframe(
    input_urls: list, input_type: str, input_sample_url: str
):
    in_driver = ogr.GetDriverByName(input_type)
    data = get_data_from_url(input_sample_url)
    in_data_source = in_driver.Open(data, 0)
    in_layer = in_data_source.GetLayer()
    in_layer_def = in_layer.GetLayerDefn()
    data_dict = {}
    for i in range(0, in_layer_def.GetFieldCount()):
        field_def = in_layer_def.GetFieldDefn(i)
        name = field_def.GetNameRef()
        data_dict[name] = []
    data_dict["geometry"] = []
    for url in input_urls:
        data = get_data_from_url(url)
        in_data_source = in_driver.Open(data, 0)
        in_layer = in_data_source.GetLayer()
        in_layer_def = in_layer.GetLayerDefn()
        for in_feature in in_layer:
            for i in range(0, in_layer_def.GetFieldCount()):
                field_def = in_layer_def.GetFieldDefn(i)
                name = field_def.GetNameRef()
                value = in_feature.GetField(i)
                data_dict[name].append(value)

            geom = in_feature.GetGeometryRef()
            geom_wkb = bytes(geom.ExportToWkb())
            shapely_geom = loads(geom_wkb)
            data_dict["geometry"].append(shapely_geom)
        in_data_source.Destroy()

    gdf = gpd.GeoDataFrame(data_dict)
    return gdf


def get_ogr_layer_object(input_file: str, input_file_type: str):
    driver = ogr.GetDriverByName(input_file_type)
    data_source = driver.Open(input_file, 0)
    layer = data_source.GetLayer()
    return layer


def get_schema_from_ogr_layer(layer, file_type) -> list:
    layer_definition = layer.GetLayerDefn()
    field_names = []
    for i in range(0, layer_definition.GetFieldCount()):
        field_defn = layer_definition.GetFieldDefn(i)
        field_name = layer_definition.GetFieldDefn(i).GetName()
        field_names.append(field_name)
    if file_type != "CSV":
        geom_field_name = None
        if layer.GetFeature(1) is not None:
            geom_ref = layer.GetFeature(1).GetGeomFieldDefnRef(0)
            if geom_ref is not None:
                geom_field_name = geom_ref.GetName()
        elif layer.GetFeature(0) is not None:
            geom_ref = layer.GetFeature(0).GetGeomFieldDefnRef(0)
            if geom_ref is not None:
                geom_field_name = geom_ref.GetName()
        if geom_field_name is not None and geom_field_name not in field_names:
            field_names.append(geom_field_name)
    return field_names


def get_all_metadata(_input: str, _type: str):
    data_source = get_datasource(_input, _type)

    metadata = {}
    for layer in data_source:
        feature_count = layer.GetFeatureCount()
        schema = get_schema_from_ogr_layer(layer, _type)
        name = layer.GetName()
        geom_type = layer.GetGeomType()
        geom_col = layer.GetGeometryColumn()
        if geom_col in schema:
            schema.remove(geom_col)

        metadata[name] = {
            "name": name,
            "geom_type": geom_type,
            "geom_col": geom_col,
            "feature_count": feature_count,
            "schema": schema,
        }
        print("here")
    return metadata


def get_datasource(_input: str, _type: str):
    driver = ogr.GetDriverByName(_type)
    if _type == "WFS":
        data_source = driver.Open(f"{_type}:{_input}")
    else:
        data_source = driver.Open(_input)
    return data_source


def get_all_layer_names(_input: str, _type: str):
    data_source = get_datasource(_input, _type)
    return [layer.GetName() for layer in data_source]


def get_layer_metadata(_input: str, _type: str, layer_name=None) -> dict:
    data_source = get_datasource(_input, _type)

    if data_source.GetLayerCount() > 1 and layer_name is None:
        raise Exception(
            "cannot get data from multi layer datasource without layer_name."
        )

    if layer_name is not None:
        layer = data_source.GetLayerByName(layer_name)
    else:
        layer = data_source.GetLayer()

    feature_count = layer.GetFeatureCount()
    schema = get_schema_from_ogr_layer(layer, _type)
    name = layer.GetName()
    geom_type = layer.GetGeomType()
    geom_col = layer.GetGeometryColumn()
    extent = layer.GetExtent()
    prj = layer.GetSpatialRef()
    srs = osr.SpatialReference(wkt=prj)

    if geom_col in schema:
        schema.remove(geom_col)

    metadata = {
        "name": name,
        "geom_type": geom_type,
        "geom_col": geom_col,
        "feature_count": feature_count,
        "schema": schema,
    }
    return metadata