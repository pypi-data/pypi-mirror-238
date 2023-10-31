from osgeo import ogr, gdal, osr
from georeader.logic.ogr_helpers import single_geom_to_multi_geom
import geopandas as gpd
import os
import logging
from shapely.wkb import loads
from random import randrange
from typing import Any

# Speeds up querying WFS capabilities for services with alot of layers
gdal.SetConfigOption('OGR_WFS_LOAD_MULTIPLE_LAYER_DEFN', 'NO')
# Set config for paging. Works on WFS 2.0 services and WFS 1.0 and 1.1 with some other services.
gdal.SetConfigOption('OGR_WFS_PAGING_ALLOWED', 'YES')
gdal.SetConfigOption('OGR_WFS_PAGE_SIZE', '10000')

LOGGER = logging.getLogger("__name__")

class OGR_Layer:
    def __init__(self, layer, driver):
        self.layer = layer
        self.driver = driver

    def get_layer_object(self):
        """
        The get_layer_object function returns the ogr.layer object of the class.

        Args:
            self: Access variables that belongs to the class

        Returns:
            The layer object of the layer that is passed in

        Doc Author:
            Trelent
        """
        return self.layer

    def get_schema(self):
        """
        The get_schema function returns a list of the field names in the schema.

        Args:
            self: Access the attributes and methods of the class in python

        Returns:
            A list of the field names in the shapefile
        """
        layer_definition = self.layer.GetLayerDefn()
        field_names = []
        for i in range(0, layer_definition.GetFieldCount()):
            field_name = layer_definition.GetFieldDefn(i).GetName()
            field_names.append(field_name)
        return field_names

    def get_schema_csv(self):
        """
        The get_schema_csv function returns a list of the field names in the layer.
        If there is a geometry column, it will be included as well.

        Args:
            self: Reference the class instance

        Returns:
            A list of the fields in a csv file
        """
        layer_definition = self.layer.GetLayerDefn()
        field_names = []
        for i in range(0, layer_definition.GetFieldCount()):
            field_name = layer_definition.GetFieldDefn(i).GetName()
            field_names.append(field_name)
        geom_field_name = None
        if self.layer.GetFeature(1) is not None:
            geom_ref = self.layer.GetFeature(1).GetGeomFieldDefnRef(0)
            if geom_ref is not None:
                geom_field_name = geom_ref.GetName()
        elif self.layer.GetFeature(0) is not None:
            geom_ref = self.layer.GetFeature(0).GetGeomFieldDefnRef(0)
            if geom_ref is not None:
                geom_field_name = geom_ref.GetName()
        if geom_field_name is not None and geom_field_name not in field_names:
            field_names.append(geom_field_name)
        return field_names

    def get_feature_count(self):
        """
        The get_feature_count function returns the number of features in a layer.

        Args:
            self: Access the class attributes

        Returns:
            The number of features in the layer

        """
        f_count = self.layer.GetFeatureCount()
        if f_count == 0:
            try:
                return len([x for x in self.layer])
            except ValueError:
                return 0
        else:
            return f_count

    def get_name(self):
        """
        The get_name function returns the name of the layer.

        Args:
            self: Refer to the object itself

        Returns:
            The name of the layer
        """
        return self.layer.GetName()

    def get_geom_type(self):
        """
        The get_geom_type function returns the geometry type of layer.

        Args:
            self: Refer to the object itself

        Returns:
            The geometry type of the layer
        """
        return self.layer.GetGeomType()

    def get_geom_col(self):
        """
        The get_geom_col function returns the name of the geometry column for a layer.

        Args:
            self: Refer to the object itself

        Returns:
            The name of the geometry column for the layer
        """
        return self.layer.GetGeometryColumn()

    def get_extent(self):
        """
        The get_extent function returns a tuple of the form (xmin, xmax, ymin, ymax)
        representing the extent of the layer.  This is useful for constructing a bounding box
        for an image.

        Args:
            self: Access the attributes and methods of the class in python

        Returns:
            A tuple containing the extent of the layer
        """
        return self.layer.GetExtent()

    def get_crs_bounds(self):
        layer_spatial_ref = self.layer.GetSpatialRef()
        spatial_ref = osr.SpatialReference()
        spatial_ref.ImportFromEPSG(4326)
        area_of_use = layer_spatial_ref.GetAreaOfUse()
        corner1 = ogr.Geometry(ogr.wkbPoint)
        corner2 = ogr.Geometry(ogr.wkbPoint)
        corner1.AddPoint(area_of_use.north_lat_degree, area_of_use.west_lon_degree)
        corner2.AddPoint(area_of_use.south_lat_degree, area_of_use.east_lon_degree)
        transform = osr.CoordinateTransformation(spatial_ref, layer_spatial_ref)
        corner1.Transform(transform)
        corner2.Transform(transform)
        return corner1.GetX(), corner1.GetY(), corner2.GetX(), corner2.GetY()

    def get_crs_code(self) -> Any:
        """
        The get_crs_code function returns the EPSG code of the coordinate reference system (CRS)
        of a layer. The function takes one argument, which is an open OGR layer object. If the CRS
        is not defined in GDAL/OGR, None is returned.

        Args:
            self: Access the attributes and methods of the class in python.

        Returns:
            The epsg code of the spatial reference system of the layer.
        """
        spatial_ref = self.layer.GetSpatialRef()
        if spatial_ref is None:
            return None
        return spatial_ref.GetAttrValue("AUTHORITY", 1)

    def get_dataframe(self, schema: list = None) -> gpd.GeoDataFrame:
        """
        The get_dataframe function returns a GeoDataFrame object from the inputted shapefile.
        The function takes in an optional schema argument, which is a list of strings that
        describe the attributes of each feature. If no schema is provided,
        the function will return all attributes for each feature.

        Args:
            self: Allow the function to refer to the object that called it
            schema:list=None: Define the schema of the dataframe

        Returns:
            geodataframe object
        """

        in_layer_def = self.layer.GetLayerDefn()
        data_dict = {}
        if schema is None:
            for i in range(0, in_layer_def.GetFieldCount()):
                field_def = in_layer_def.GetFieldDefn(i)
                name = field_def.GetNameRef()
                data_dict[name] = []
        else:
            for attr_name in schema:
                data_dict[attr_name] = []
        data_dict["geometry"] = []
        schema = list(data_dict.keys())
        for in_feature in self.layer:
            for attr_name in schema:
                if attr_name != "geometry":
                    data_dict[attr_name].append(in_feature.GetField(attr_name))

            geom = in_feature.GetGeometryRef()
            geom = geom.Normalize()
            geom_wkb = bytes(geom.ExportToWkb())
            shapely_geom = loads(geom_wkb)
            data_dict["geometry"].append(shapely_geom)
        gdf = gpd.GeoDataFrame(data_dict)
        return gdf

    def convert(self, out_file, out_type):
        """
        The convert function takes an input file and converts it to a specified output type.
        The convert function accepts two parameters: out_file, the name of the output file;
        and out_type, the type of file to be created.

        Args:
            self: Reference the class instance
            out_file: Specify the output file name
            out_type: Specify the output file type

        Returns:
            The out_data_source
        """
        try:
            self._layer_features_valid()
        except Exception as e:
            raise Exception('failed to get convert layer, cannot read features') from e

        def copy_features(_in_layer, _out_layer):
            for in_feature in _in_layer:
                _out_layer.CreateFeature(in_feature)
            return _out_layer

        def copy_field_definitions(_in_layer, _out_layer):
            _in_layer_def = _in_layer.GetLayerDefn()
            for i in range(0, _in_layer_def.GetFieldCount()):
                field_def = _in_layer_def.GetFieldDefn(i)
                _out_layer.CreateField(field_def)
            return _out_layer

        out_driver = ogr.GetDriverByName(out_type)
        out_data_source = out_driver.CreateDataSource(out_file)
        out_lyr_name = os.path.splitext(os.path.split(out_file)[1])[0]
        out_layer = out_data_source.CreateLayer(out_lyr_name)

        copy_field_definitions(self.layer, out_layer)
        copy_features(self.layer, out_layer)

    def get_normalized_geom_type(self):
        """
        The get_normalized_geom_type function returns the geometry type of feature in a layer.
        The function first gets the feature from the layer, then it normalizes that geometry, and finally it returns
        the normalized geometry's type.

        Args:
            self: Access variables that belongs to the class

        Returns:
            The type of the geometry
        """
        count = self.get_feature_count()
        feature = self.layer.GetFeature(count-1)
        geom = feature.GetGeometryRef()
        normalized_geom = geom.Normalize()
        if self.driver == "ESRI Shapefile":
            multi_geom = single_geom_to_multi_geom(normalized_geom)
            geom_type = multi_geom.GetGeometryType()
        else:
            geom_type = normalized_geom.GetGeometryType()
        return geom_type

    def write_to_postgis_db(self,
                            table_name: str,
                            connection_string: str,
                            schema: str = 'public',
                            crs: int = None,
                            overwrite: bool = False,
                            force_type: int = None):
        """
        The write_to_postgis_db function writes a vector layer to a postgis database.
        The function takes the following parameters:
            table_name: The name of the table that will be created in the database. This is required and must be unique for each layer you want to write to your database unless overwrite is True
            connection_string: A string containing all necessary information for connecting with your postgis db server, including user, password, host and port if not using localhost (default).
                For example "PG:dbname=test user=postgres password=password host='localhost' port='5432'";

        Args:
            self: Reference the class instance
            table_name:str: Name the table in postgis
            connection_string:str: Connect to the database
            schema:str='public': Specify the schema in which to create the table
            crs:int=None: Set the crs of the layer
            overwrite:bool=False: Determine if the table should be overwritten or not
            force_type:int=None: force a geom type for layer if not will it will use the geom type
                of the first feature found.
        Returns:
            None
        """

        if crs is None:
            srs = self.layer.GetSpatialRef()
            if srs.GetName() is None:
                raise ValueError(f'layer does not have a crs one must be provided.')

        if crs is not None:
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(crs)
            if srs.GetName() is None:
                raise ValueError(f'"{crs}" is not a valid crs')

        db_datastore = ogr.Open(connection_string)
        if db_datastore is None:
            raise ValueError('Something went wrong trying to connect to database. please connection string is correct')

        db_datastore.StartTransaction()
        try:
            geom_type = force_type if force_type is not None else self.get_normalized_geom_type()
            full_table_name = f'{schema}.{table_name}'
            overwrite_val = 'OVERWRITE=YES' if overwrite else 'OVERWRITE=NO'
            layer_creation_opts = [overwrite_val,
                                   'GEOMETRY_NAME=geometry',
                                   'FID=GID',
                                   'LAUNDER=NO'
                                   ]
            out_layer = db_datastore.CreateLayer(
                full_table_name,
                srs,
                geom_type,
                layer_creation_opts
            )
            if out_layer is None:
                raise ValueError('Layer already exists')

            layer_def = self.layer.GetLayerDefn()
            for i in range(0, layer_def.GetFieldCount()):
                field_def = layer_def.GetFieldDefn(i)
                out_layer.CreateField(field_def)
            out_layer_defn = out_layer.GetLayerDefn()

            for in_feature in self.layer:
                out_feature = ogr.Feature(out_layer_defn)
                for i in range(0, layer_def.GetFieldCount()):
                    out_feature.SetField(out_layer_defn.GetFieldDefn(i).GetNameRef(), in_feature.GetField(i))
                geom = in_feature.GetGeometryRef()
                geom = geom.Normalize()
                if self.driver == 'ESRI Shapefile' and force_type is None:
                    geom = single_geom_to_multi_geom(geom)
                out_feature.SetGeometry(geom.Clone())
                out_layer.CreateFeature(out_feature)
                out_feature = None
            db_datastore.CommitTransaction()
        except Exception as e:
            db_datastore.RollbackTransaction()
            raise Exception('failed to write to db') from e





