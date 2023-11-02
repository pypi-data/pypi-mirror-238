import json 
import re 
import os
from abstract_utilities import read_from_file
def try_json_load(file):
    try:
        return json.load(file)
    except json.JSONDecodeError:
        return None
def try_json_loads(data):
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return None
def all_try(function=None, data=None, var_data=None, error=False, error_msg=None, error_value=Exception, attach=None, attach_var_data=None):
    try:
        if not function:
            raise ValueError("Function is required")

        if var_data and not data:
            result = function(**var_data)
        elif data and not var_data:
            if attach and attach_var_data:
                result = function(data).attach(**attach_var_data)
            else:
                result = function(data).attach() if attach else function(data)
        elif data and var_data:
            raise ValueError("Both data and var_data cannot be provided simultaneously")
        else:
            result = function()
        return result
    except error_value as e:
        if error:
            raise e
        elif error_msg:
            print_error_msg(error_msg, f': {e}')
        return False
def all_try_json_loads(data, error=False, error_msg=None, error_value=(json.JSONDecodeError, TypeError)):
    return all_try(data=data, function=json.loads, error=error, error_msg=error_msg, error_value=error_value)

def safe_json_loads(data, default_value=None, error=False, error_msg=None): 
    """ Safely attempts to load a JSON string. Returns the original data or a default value if parsing fails.
    Args:
        data (str): The JSON string to parse.
        default_value (any, optional): The value to return if parsing fails. Defaults to None.
        error (bool, optional): Whether to raise an error if parsing fails. Defaults to False.
        error_msg (str, optional): The error message to display if parsing fails. Defaults to None.
    
    Returns:
        any: The parsed JSON object, or the original data/default value if parsing fails.
    """
    try_json = all_try_json_loads(data=data, error=error, error_msg=error_msg)
    if try_json:
        return try_json
    if default_value:
        data = default_value
    return data
def clean_invalid_newlines(json_string: str,line_replacement_value='') -> str: 
    """ Removes invalid newlines from a JSON string that are not within double quotes.
    Args:
        json_string (str): The JSON string containing newlines.
    
    Returns:
        str: The JSON string with invalid newlines removed.
    """
    pattern = r'(?<!\\)\n(?!([^"]*"[^"]*")*[^"]*$)'
    return re.sub(pattern, line_replacement_value, json_string)
def get_value_from_path(json_data, path,line_replacement_value='*n*'): 
    """ Traverses a nested JSON object using a specified path and returns the value at the end of that path.
    Args:
        json_data (dict/list): The JSON object to traverse.
        path (list): The path to follow in the JSON object.
    
    Returns:
        any: The value at the end of the specified path.
    """
    current_data = safe_json_loads(json_data)
    for step in path:
        current_data = safe_json_loads(current_data[step])
        if isinstance(current_data, str):
            current_data = read_malformed_json(current_data,line_replacement_value=line_replacement_value)
    return current_data
def find_paths_to_key(json_data, key_to_find,line_replacement_value='*n*'): 
    """ Searches a nested JSON object for all paths that lead to a specified key.
    Args:
        json_data (dict/list): The JSON object to search.
        key_to_find (str): The key to search for in the JSON object.
    
    Returns:
        list: A list of paths (each path is a list of keys/indices) leading to the specified key.
    """
    def _search_path(data, current_path):
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = current_path + [key]
                if key == key_to_find:
                    paths.append(new_path)
                if isinstance(value, str):
                    try:
                        json_data = read_malformed_json(value,line_replacement_value=line_replacement_value)
                        _search_path(json_data, new_path)
                    except json.JSONDecodeError:
                        pass
                _search_path(value, new_path)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                new_path = current_path + [index]
                _search_path(item, new_path)
    
    paths = []
    _search_path(json_data, [])
    return paths
def read_malformed_json(json_string,line_replacement_value="*n"): 
    """ Attempts to parse a malformed JSON string after cleaning it.
    Args:
        json_string (str): The malformed JSON string.
    
    Returns:
        any: The parsed JSON object.
    """
    if isinstance(json_string, str):
        json_string = clean_invalid_newlines(json_string,line_replacement_value=line_replacement_value)
    return safe_json_loads(json_string)
def get_any_value(json_obj, key,line_replacement_value="*n*"): 
    """ Fetches the value associated with a specified key from a JSON object or file. If the provided input is a file path, it reads the file first.
    Args:
        json_obj (dict/list/str): The JSON object or file path containing the JSON object.
        key (str): The key to search for in the JSON object.
    
    Returns:
        any: The value associated with the specified key.
    """
    if isinstance(json_obj,str):
        if os.path.isfile(json_obj):
            json_obj = read_from_file(json_obj)
    json_data = read_malformed_json(json_obj)
    paths_to_value = find_paths_to_key(json_data, key)
    if not isinstance(paths_to_value, list):
        paths_to_value = [paths_to_value]
    for i, path_to_value in enumerate(paths_to_value):
        paths_to_value[i] = get_value_from_path(json_data, path_to_value)
        if isinstance(paths_to_value[i],str):
            paths_to_value[i]=paths_to_value[i].replace(line_replacement_value,'\n')
    if len(paths_to_value) == 1:
        paths_to_value = paths_to_value[0]
    return paths_to_value
class FileCollator:
    def __init__(self,files_list,key_value=None):
        self.files_list=files_list or []
        self.key_value=key_value or []
    def get_gollated_responses(self,files_list=None,key_value=None):
        if files_list == None:
            files_list=self.files_list
        if key_value == None:
            key_value=self.key_value
        files = self.get_json_data(files_list,key_value=key_value)
        collated_string = self.collate_responses(files)
        return collated_string
    def collate_responses(self,files_list):
        collate_str=''
        nix_list=[]
        for each in files_list:
            lowest = self.get_oldest_first(files_list,nix_list=nix_list)
            nix_list.append(lowest[0])
            collate_str +='\n'+str(files_list[lowest[0]]["value"])
        return collate_str
    @staticmethod
    def get_json_data(files_list,key_value=None):
        if key_value == None:
            key_value='content'
        files = []
        for file_path in files_list:
            api_response = get_any_value(file_path,key_value)
            files.append({'created':int(get_any_value(file_path ,'created')),"value":api_response})
        return files
    @staticmethod
    def get_oldest_first(json_list,nix_list=[]):
        lowest=[None,None]
        for i,values in enumerate(json_list):
            if i not in nix_list:
                if lowest[0] == None:
                    lowest=[i,values['created']]
                elif values['created'] < lowest[1]:
                    lowest=[i,values['created']]
        return lowest

