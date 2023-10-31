import configparser

config = configparser.ConfigParser()
import geopandas.geodataframe as geodataframe
import georeader.logic.ogr_helpers as helpers


class Converters:

    # GML Converters
    @staticmethod
    def convert_gml_to_shape_file(input_file: str, output_file: str) -> str:
        """
        The convert_gml_to_shape_file function converts a GML file to a shapefile.

        Args:
            input_file:str: Specify the input file that will be converted to a shapefile
            output_file:str: Specify the output file name

        Returns:
            The name of the output file
        """
        return helpers.convert_multiple_files_to_file(
            input_files=[input_file],
            input_type="GML",
            output_file=output_file,
            output_file_type="ESRI Shapefile",
        )

    @staticmethod
    def convert_multiple_gml_to_shape_file(
        input_files: list, input_sample_file: str, output_file: str
    ) -> str:
        """
        The convert_multiple_gml_to_shape_file function converts multiple GML files to a single ESRI Shapefile.
        The function takes three arguments:
            input_files (list): A list of the paths to the input files.
            input_sample_file (str): The path to an example file that contains all of the fields that should be present in the output file. This is used as a template for populating those fields in each output record, and also as a means of validating whether or not all records have been successfully converted.
            output_file (str): The path where you want your final ESRI Shapefile written.

        Args:
            input_files:list: Pass a list of input files to the function
            input_sample_file:str: Provide a sample file to the function
            output_file:str: Specify the name of the output file

        Returns:
            The output file path
        """
        return helpers.convert_multiple_files_to_file(
            input_files=input_files,
            input_type="GML",
            output_file=output_file,
            output_file_type="ESRI Shapefile",
            input_sample_file=input_sample_file,
        )

    @staticmethod
    def convert_gml_to_gpkg(input_file: str, output_file: str) -> str:
        """
        The convert_gml_to_gpkg function converts a GML file to a GeoPackage.

        Args:
            input_file:str: Specify the input file
            output_file:str: Specify the output file

        Returns:
            The path to the output file
        """
        return helpers.convert_multiple_files_to_file(
            input_files=[input_file],
            input_type="GML",
            output_file=output_file,
            output_file_type="GPKG",
        )

    @staticmethod
    def convert_multiple_gml_to_gpkg(
        input_files: list, input_sample_file: str, output_file: str
    ) -> str:
        """
        The convert_multiple_gml_to_gpkg function converts multiple GML files to a GPKG file.
        The function accepts a list of input files, an output file name, and an input sample file.
        It returns the path to the converted GPKG file.

        Args:
            input_files:list: Pass a list of files to be converted
            input_sample_file:str: Get the schema of the input file
            output_file:str: Specify the output file name

        Returns:
            A string that is the path to the output file
        """
        return helpers.convert_multiple_files_to_file(
            input_files=input_files,
            input_type="GML",
            output_file=output_file,
            output_file_type="GPKG",
            input_sample_file=input_sample_file,
        )

    @staticmethod
    def convert_gml_to_geojson(input_file: str, output_file: str):
        """
        The convert_gml_to_geojson function converts a GML file to GeoJSON.

        Args:
            input_file:str: Specify the input file
            output_file:str: Specify the output file name

        Returns:
            A geojson file
        """
        return helpers.convert_multiple_files_to_file(
            input_files=[input_file],
            input_type="GML",
            output_file=output_file,
            output_file_type="GEOJSON",
        )

    @staticmethod
    def convert_multiple_gml_to_geojson(
        input_files: list, input_sample_file: str, output_file: str
    ) -> str:
        """
        The convert_multiple_gml_to_geojson function converts multiple GML files to a single GeoJSON file.

        Args:
            input_files:list: Pass a list of files that will be converted to geojson
            input_sample_file:str: Get the schema of the input file
            output_file:str: Specify the output file name

        Returns:
            A string that is the path to the output file
        """
        return helpers.convert_multiple_files_to_file(
            input_files=input_files,
            input_type="GML",
            output_file=output_file,
            output_file_type="GEOJSON",
            input_sample_file=input_sample_file,
        )

    @staticmethod
    def convert_multiple_gml_to_dataframe(
        input_files: list, input_sample_file: str
    ) -> geodataframe:
        """
        The convert_multiple_gml_to_dataframe function converts multiple GML files to a GeoDataFrame.
        The function takes two arguments: input_files and input_sample_file. The input_files argument is a list of the file paths for each GML file that will be converted to a GeoDataFrame. The second argument, input_sample_file, is the path for one of the files in the list of files that will be used to infer column names and data types from when converting all of the other GML files into GeoDataFrames.

        Args:
            input_files:list: Specify a list of input files to be converted
            input_sample_file:str: Get the geometry type of the input data

        Returns:
            A geodataframe

        Doc Author:
            Trelent
        """
        return helpers.convert_multiple_files_to_dataframe(
            input_files=input_files,
            input_type="GML",
            input_sample_file=input_sample_file,
        )

    # ESRI REST Converters
    @staticmethod
    def convert_esri_rest_to_shape_file(
        input_urls: list, input_sample_url, output_file
    ) -> str:
        """
        The convert_esri_rest_to_shape_file function converts a list of ESRI JSON URLs to an ESRI Shapefile.
        The function takes three arguments:
            input_urls - A list of URLs to the data that will be converted into a shapefile.  The data must be in the ESRIJSON format.
            input_sample_url - A URL to an example dataset that is in the same format as what you want converted into a shapefile (i.e., if your input urls are geotiffs, then this should be a geotiff).  This is used for metadata purposes only, and can contain any arbitrary string value (

        Args:
            input_urls:list: Specify the urls of the esrijson files that will be converted to shapefile
            input_sample_url: Get the spatial reference of the input data
            output_file: Specify the output file name

        Returns:
            A string

        Doc Author:
            Trelent
        """
        return helpers.convert_multiple_urls_to_file(
            input_urls=input_urls,
            input_type="ESRIJSON",
            input_sample_url=input_sample_url,
            output_file=output_file,
            output_file_type="ESRI Shapefile",
        )

    @staticmethod
    def convert_esri_rest_to_dataframe(
        input_urls: list, input_sample_url: str
    ) -> geodataframe:
        """
        The convert_esri_rest_to_dataframe function takes a list of ESRI JSON URLs and returns a GeoDataFrame.
        The function also accepts an optional sample URL from which it can extract the spatial reference information
        for the output GeoDataFrame.

        Args:
            input_urls:list: Pass a list of urls to the function
            input_sample_url:str: Get the schema of the data

        Returns:
            A geodataframe
        """
        return helpers.convert_multiple_urls_to_dataframe(
            input_urls=input_urls,
            input_type="ESRIJSON",
            input_sample_url=input_sample_url,
        )

    @staticmethod
    def convert_geojson_to_shapefile(input_file: str, output_file: str):
        return helpers.convert_multiple_files_to_file(
            input_files=[input_file],
            input_type="GEOJSON",
            output_file=output_file,
            output_file_type="ESRI Shapefile",
        )

    @staticmethod
    def convert_multiple_geojson_to_dataframe(input_files: list) -> geodataframe:
        """
        The convert_multiple_geojson_to_dataframe function takes a list of geojson files and returns a pandas dataframe.
        The function also allows for the user to specify the column names in the resulting dataframe.

        Args:
            input_files:list: Specify the list of geojson files that will be converted to a dataframe

        Returns:
            A geodataframe
        """
        return helpers.convert_multiple_files_to_dataframe(
            input_files=input_files, input_type="GEOJSON"
        )

    @staticmethod
    # schemas
    def get_schema_from_file(input_file: str, input_type: str) -> list:
        """
        The get_schema_from_file function takes a file path and the type of file (json or csv)
        and returns a list of dictionaries, where each dictionary represents one row in the input
        file. The function is used to parse data from files into lists that can be processed by
        the functions in this module.

        Args:
            input_file:str: Specify the file that contains the data to be loaded into a table
            input_type:str: Determine which type of file is being read

        Returns:
            A list of dictionaries
        """
        return helpers.get_schema_from_file(input_file, input_type)
