import json
import os
import requests
from abstract_utilities import (get_date,
                                get_time_stamp,
                                mkdirs,
                                safe_write_to_json,
                                json_key_or_default,
                                get_files,
                                unified_json_loader,
                                safe_json_loads,
                                safe_read_from_json,
                                
                                find_keys,
                                get_file_create_time,
                                
                                find_paths_to_key,

                                make_bool,
                                get_highest_value_obj,
                                make_list
                                )

from abstract_utilities import create_new_name,unified_json_loader,get_sleep,eatAll,safe_json_loads,read_from_file,safe_dump_to_file
from abstract_gui import get_browser
import nltk
#!/usr/bin/env python3
"""
json_utils.py

This script is a utility module providing functions for handling JSON data. It includes functionalities like:
1. Converting JSON strings to dictionaries and vice versa.
2. Merging, adding to, updating, and removing keys from dictionaries.
3. Retrieving keys, values, specific items, and key-value pairs from dictionaries.
4. Recursively displaying values of nested JSON data structures with indentation.
5. Loading from and saving dictionaries to JSON files.
6. Validating and cleaning up JSON strings.
7. Searching and modifying nested JSON structures based on specific keys, values, or paths.
8. Inverting JSON data structures.
9. Creating and reading from JSON files.

Each function is documented with Python docstrings for detailed usage instructions.

This module is part of the `abstract_utilities` package.

Author: putkoff
Date: 05/31/2023
Version: 0.1.2
"""
import json
import re
import os
from typing import List, Union, Dict, Any

class SaveManager:
    """
    Manages the saving of data. This class should provide methods to specify where (e.g., what database or file) and how (e.g., in what format) data should be saved.
    """
    def __init__(self,api_response={},title=None,directory=None):
        self.api_response=safe_json_loads(api_response)
        self.title = title
        self.model= get_any_key(self.api_response,'model') or 'default'
        self.created = get_any_key(self.api_response,'created')
        self.content = get_any_key(self.api_response,'content')
        self.generate_title = get_any_key(self.content,'generate_title')
        self.date = get_date()
        self.title = self.title or self.generate_title or self.created
        self.directory = mkdirs(directory or os.path.join(os.getcwd(),'response_data'))
        if get_any_key(self.content,'error'):
            self.fold_model= mkdirs(os.path.join(self.directory,self.date,'error'))
            self.title = self.create_unique_title(title=self.title,directory=self.fold_model)
            self.file_name = f'{self.title}.json'
        
        else:

            self.fold_model= mkdirs(os.path.join(self.directory,self.date,self.model))
            self.title = self.create_unique_title(title=self.title,directory=self.fold_model)
            self.file_name = f'{self.title}.json'
        self.file_path = os.path.join(self.fold_model,self.file_name)
        safe_dump_to_file(file_path=self.file_path,data=self.api_response)
    def create_unique_title(self,title:str=None,directory:str=None):
        """
        Generates a unique title by appending an index number to the given base title.

        Args:
            title (str, optional): The base title to start with. Defaults to a timestamp-based string.
            directory (str, optional): The directory to search for existing titles. Defaults to the current working directory.

        Returns:
            A unique title string formed by appending an index number to the base title.
        """
        title_new = title or self.title or str(get_time_stamp())
        directory = directory or self.directory or os.path.join(os.getcwd(),'response_data')
        files = get_files(directory)
        all_files = []
        for file in files:
            base_name = os.path.basename(file)
            all_files.append(base_name)
            file_name,ext=os.path.splitext(base_name)
            if file_name not in all_files:
                all_files.append(file_name)
        i=0
        while title_new in all_files:
            title_new=title+f'_{i}'
            i+=1
        return title_new

class ResponseManager:
    """
    Handles the management of responses received from the models. This could include interpreting and formatting the responses, managing errors, and handling special cases.
    """
    def __init__(self,prompt_mgr,api_mgr,title=None,directory=None):
        self.prompt_mgr=prompt_mgr
        self.model_mgr=self.prompt_mgr.model_mgr
        self.api_mgr=api_mgr
        self.title=title
        self.directory = mkdirs(directory or os.path.join(os.getcwd(),'response_data'))
        self.bot_notation=None
        self.token_dist =prompt_mgr.token_dist
        self.output=[]
        self.i_query=0
        self.query_done=False
    def post_request(self):
        """
        Sends a POST request to the specified endpoint with the provided prompt and headers.
        
        Args:
            endpoint (str): URL endpoint to which the request is sent.
            prompt (str or dict): Prompt or data to be sent in the request.
            content_type (str): Type of the content being sent in the request.
            api_key (str): The API key for authorization.
            header (dict): Optional custom headers. If not provided, default headers will be used.
            
        Returns:
            dict: Response received from the server.
        """
        if self.response.status_code == 200:
            print(f'Request successful with status code {self.api_response.status_code}')
        else:
            raise Exception(f'Request failed with status code {self.api_response.status_code}\n{self.api_response.text}\n\n')
        return self.get_response()
    def get_response(self):
        """
        Extracts and returns the response dictionary from the API response.

        Returns:
            dict: Extracted response dictionary.
        """
        try:
            self.api_response = self.response.json()
        except:
            self.api_response = self.response.text
        return self.api_response
    def try_load_response(self):
        self.api_response = safe_json_loads(self.get_response())
        self.content = safe_json_loads(find_keys(self.api_response,'content'))
        if self.content:
            if isinstance(self.content,list):
                self.content = safe_json_loads(self.content[0])
    def extract_response(self):
        self.query_js={}
        self.query_js["prompt"]=safe_json_loads(self.prompt)
        self.query_js["response"] = safe_json_loads(self.api_response)
        self.save_manager = SaveManager(api_response=self.api_response,title=self.title,directory=self.directory)
        self.query_js["title"]=self.save_manager.title
        self.output.append(self.query_js)
        return self.query_js
    def get_last_response(self):
        self.recent_file = get_highest_value_obj(get_files(self.directory),function=get_file_create_time)
        self.last_response = safe_json_loads(safe_read_from_json(self.recent_file))
        self.content = safe_json_loads(get_any_key(self.api_response,'content'))
        self.response_js= safe_json_loads(get_any_key(self.content, 'api_response'))
        return self.recent_file,self.response_js
    def get_response_bools(self):
        response_bool_js = {"abort":get_any_key(self.content, "abort") or False,
                            "additional_response":get_any_key(self.content, "additional_response") or False}
        for key,value in response_bool_js.items():
            if isinstance(value,str):
               response_bool_js[key]=eatAll(value,['\n','\t',' ',''])
            response_bool_js[key]=make_bool(response_bool_js[key])
        self.abort_it =response_bool_js['abort']
        self.additional_response_it = response_bool_js['additional_response']
        self.bot_notation = get_any_key(self.content, "notation")
    def send_query(self,i):
        self.prompt = self.prompt_mgr.create_prompt(dist_number=i,bot_notation=self.bot_notation)
        self.endpoint =self.model_mgr.selected_endpoint
        self.header=self.api_mgr.header
        self.response = requests.post(url=self.endpoint,json=self.prompt,headers=self.header)
        self.prepare_response()
    def test_query(self,i):
        self.response = self.get_last_response(file=test)[0]
        self.prepare_response(test=test)
    def prepare_response(self):
        self.try_load_response()
        self.extract_response()
        self.recent_file,self.response_js = self.get_last_response()
        self.get_response_bools()
    def initial_query(self):
        self.query_done=False
        self.i_query = 0
        for i in range(len(self.token_dist)):
            response_loop=True
            abort_it=False
            while response_loop:
                self.send_query(i)
                if not self.additional_response_it or self.abort_it:
                    response_loop = False
                    break
                print(f'in while {i}')
            if self.abort_it:
                break
            self.i_query=i
        self.query_done=True
        self.i_query=0
        return self.output

