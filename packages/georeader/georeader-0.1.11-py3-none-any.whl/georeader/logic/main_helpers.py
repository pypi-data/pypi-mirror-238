import re
import pathlib
import logging
import os
import sys
from typing import Any

log = logging.getLogger(__name__)


def match_on(key: str, string: str):
    """
    The match_on function takes a key and a string as arguments.
    It then searches for the key in the string, returning any matches found.

    Args:
        key:str: Specify the key in the dictionary to be used
        string:str: Pass the string to be searched through

    Returns:
        A match object
    """
    return re.search(f'({key}=([a-z-A-Z-0-9_"£$%*^~])+)', string)


def get_property_like(data_dict: dict, like_key: str, on_fail: Any) -> Any:
    """
    The get_property_like function takes a dictionary and a string.
    It returns the value of the key in the dictionary that contains all or part of like_key.
    If no such key exists, it returns on_fail.

    Args:
        data_dict:dict: Pass the dictionary that is being searched
        like_key:str: Search for a key that contains the like_key string
        on_fail:Any: Return a value if no key is found

    Returns:
        The value of the key that has a string similar to the like_key
    """
    for key in data_dict:
        if like_key in key.lower():
            return data_dict[key]
    return on_fail


def remove_key(d: dict, key: str):
    """
    The remove_key function removes a key from a dictionary.

    Args:
        d:dict: Specify the dictionary that is to be modified
        key:str: Specify which key to remove from the dictionary

    Returns:
        A dictionary with the key removed
    """
    r = dict(d)
    del r[key]
    return r


def get_item_from_nested_dict(data_dict, params=[]):
    """
    The get_item_from_nested_dict function takes a dictionary and a list of parameters.
    It returns the value of the nested dictionary at the location specified by those parameters, or None if it doesn't exist.

    Args:
        data_dict: Store the nested dictionary
        params=[]: Specify the path to the desired item in data_dict

    Returns:
        The value of the last key in params if it exists
    """
    for param in params:
        new_data_dict = get_property_like(data_dict, param, None)
        if new_data_dict is not None:
            data_dict = new_data_dict
        else:
            return None
    return new_data_dict


def get_json_safely(response):
    """
    The get_json_safely function takes a response object as an argument and returns the JSON
    of that response if the status code is 200. If it's not, it raises an exception with the error
    message from the API.

    Args:
        response: Get the json from the api

    Returns:
        The json of the response if the status code is 200
    """
    # bad status code
    if response.status_code != 200:
        response.raise_for_status()

    json = response.json()  # get the JSON
    if "error" in json:
        raise ValueError(f"Error: {json['error']}")
    return json


def get_file_ext(url):
    """
    gets the extension of a file.
    """
    suffix = pathlib.Path(url).suffix
    if suffix.strip() == "":
        return None
    else:
        return suffix.lower()[1:]


def rename_df_columns(data_frame, new_schema):
    """datatakes in dataframe and gets original column names from wfs schema and updates them.

    Args:
        data_frame (geopandas.dataframe): the dataframe to have columns renamed
        type_name (string]): type_name so wfs is able to get get correct column names
    Returns:
        geopandas.dataframe: geopandas dataframe with renamed column names
    """
    current_schema = [x for x in data_frame.columns]
    checked = []
    renamed_columns = {}
    for x in new_schema:
        for y in current_schema:
            if y in x and y not in checked:
                renamed_columns[y] = x
                checked.append(y)
                break
            else:
                if y not in checked:
                    checked.append(y)
        else:
            continue
    data_frame = data_frame.rename(columns=renamed_columns)
    return data_frame


def generate_params_str(param_list: list) -> str:
    """
    The generate_params_str function takes a list of tuples and returns a string
    representation of the parameters. The first element in each tuple is the parameter name,
    and the second element is its value. If there are multiple parameters, they are joined with an ampersand.

    Args:
        param_list:list: Store the parameters that will be used in the query

    Returns:
        A string of parameters in the format '?param=value&amp;param2=value2'
    """
    param_str = ""
    for param in param_list:
        sign = "?" if param_str == "" else "&"
        param_str = f"{param_str}{sign}{param[0]}={param[1]}"
    return param_str


def winapi_path(dos_path: str, encoding=None) -> str:
    r"""
    The winapi_path function is used to convert paths longer than 255 characters into a format that
    is supported by Windows.  The function takes the path as an argument and returns the converted
    path.  If the path starts with \\\\ then it adds \\?\UNC\ to the beginning of the path, otherwise
    it adds \\?\.

    Args:
        dos_path:str: Pass the path of a file or directory
        encoding=None: Specify the encoding of the file

    Returns:
        A string that is the absolute path of the given dos_path
    """
    path = os.path.abspath(dos_path)
    if path.startswith("\\\\"):
        path = "\\\\?\\UNC\\" + path[2:]
    else:
        path = "\\\\?\\" + path
    return path


def fix_long_path_win(path: str) -> str:
    """
    The fix_long_path_win function fixes paths that are too long for Windows.

    Args:
        path:str: Store the path to the file that is being processed

    Returns:
        The path with the extra long paths
    """
    if sys.platform.startswith("win") and len(path) > 255:
        return winapi_path(path)
    else:
        return path
