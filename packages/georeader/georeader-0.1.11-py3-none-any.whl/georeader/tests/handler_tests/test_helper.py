import os
from pathlib import Path

tests_root_dir = Path(os.path.abspath(__file__)).parent.parent


def create_test_folder():
    f_dir = os.path.join(tests_root_dir, 'data')
    folder = os.path.join(f_dir, f'temp_files/test_files')
    if not os.path.exists(folder):
        os.mkdir(folder)
    return folder


def create_test_files(gdal_driver, extension):
    f_dir = os.path.join(tests_root_dir, 'data')
    files = [f for f in os.listdir(f_dir) if os.path.isfile(os.path.join(f_dir, f))]
    test_file_dir = create_test_folder()
    for f in files:
        f_name = os.path.splitext(f)[0]
        create_f_name = os.path.join(test_file_dir, f"{f_name}.{extension}")
        ogr_helpers.convert_multiple_files_to_file(
            input_files=[polygon_file],
            input_type="GEOJSON",
            output_file=polygon_shapefile,
            output_file_type="ESRI Shapefile",
        )







if __name__ == "__main__":
    create_test_files('hello')