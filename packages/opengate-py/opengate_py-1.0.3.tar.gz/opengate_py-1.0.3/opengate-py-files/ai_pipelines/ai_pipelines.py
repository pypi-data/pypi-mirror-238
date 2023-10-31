'''  AIPipelinesBuilder '''
# pylint: disable=E0401
# pylint: disable=W0611
# pylint: disable=C0303
# pylint: disable=W0105
# pylint: disable=C0301

import requests
import os
import configparser
import json
import urllib3
import re
from dotenv import load_dotenv, dotenv_values, set_key
from typing import Callable, Union, List, Dict, Any

class AIPipelinesBuilder:
    ''' Builder pipelines '''
    def __init__(self, opengate_client: str):
        self.client: str = opengate_client
        self.organization_name: str = None
        self.identifier: str = None
        self.config_file: str = None
        self.section: str = None
        self.config_key: str = None
        self.data_env: str = None
        self.new_file: str = None
        self.data_prediction: dict = None
        self.url: str = None
        self.requires: Dict[str, Any] = None
        self.method: str = None
        self.name: str = None
        self.find_name: str = None
        self.output_file_path: str = None
        self.file_name: str = None
        self.collect = None
        self.action = None
        self.type = None
        self.actions = []

    def with_organization(self, organization_name: str) -> 'AIPipelinesBuilder':
        ''' User organization '''
        self.organization_name = organization_name
        return self
    
    def with_identifier(self, identifier: str) -> 'AIPipelinesBuilder':
        ''' Transformer Identifier '''
        self.identifier = identifier
        return self
    
    def with_config_file(self,config_file: str, section: str, config_key: str) -> 'AIPipelinesBuilder':
        ''' config file. '''
        self.config_file = config_file
        self.section = section
        self.config_key = config_key
        return self
    
    def with_env(self, data_env: str) -> 'AIPipelinesBuilder':
        ''' env '''
        self.data_env = data_env
        return self
    
    def with_find_by_name(self, find_name: str) -> 'AIPipelinesBuilder':
        ''' Find transformer by name '''
        self.find_name = find_name
        return self
    
    def with_prediction(self, data_prediction: dict) -> 'AIPipelinesBuilder':
        ''' Prediction data '''
        self.data_prediction = data_prediction
        return self
    
    def with_file_name(self, file_name: str) -> 'AIPipelinesBuilder':
        ''' file_name '''
        self.file_name = file_name
        return self
    
    def with_collect(self, collect: dict) -> 'AIPipelinesBuilder':
        ''' Name and actions, for creating a pipeline '''
        self.collect = collect
        return self
    
    def with_name(self, name: str) -> 'AIPipelinesBuilder':
        ''' Add name pipelines '''
        self.name = name
        return self
    
    def add_action(self, file_name: str, type=None):
        ''' add action name and type de model or transform exist'''

        if os.path.dirname(file_name):
            file_name = os.path.basename(file_name)
        
        _, file_extension = os.path.splitext(file_name)
        if file_extension == '.py':
            default_type = 'TRANSFORMER'
        else:
            default_type = 'MODEL'
        
        action_type = type if type is not None else default_type 

        action = {
            'name': file_name,
            'type': action_type
        }
        self.actions.append(action)

        return self

    def create(self) -> 'AIPipelinesBuilder':
        '''Create a transformer and have the option to incorporate the with_config_file function, 
           to modify its pipeline_id in the configuration file'''
        self.requires = {
            'organization': self.organization_name,
            'name': self.name,
            'action': self.actions
        }
        self.url = f'{self.client.url}/north/ai/{self.organization_name}/pipelines'
        self.method = 'create'
        return self

    def find_all(self) -> 'AIPipelinesBuilder':
        ''' Retrieve all the pipelines '''
        self.requires = {
            'organization': self.organization_name
        }
        self.url = f'{self.client.url}/north/ai/{self.organization_name}/pipelines'
        self.method = 'find_all'
        return self

    def _get_identifier(self):
        if self.identifier is not None:
            return self.identifier
        
        elif self.data_env is not None:
            try:
                config = dotenv_values()
                return config.get(self.data_env)
            except:
                raise ValueError('The parameter was not found in the configuration env')

        if self.config_file is not None and self.section is not None and self.config_key is not None :
            try:
                return self._read_config_file().get(self.section,self.config_key)
            except configparser.NoOptionError:
                return ValueError('The "pipeline_id" parameter was not found in the configuration file.')

        if self.find_name is not None:
            all_identifiers = self.find_all().build().execute().json()
            name_identifier = [item['identifier'] for item in all_identifiers if item['name'] == self.find_name]

            if not name_identifier:
                raise ValueError('File name does not exist')

            return name_identifier[0]

        raise ValueError('A configuration file with identifier, a model identifier or a find by name is required.')
    
    def find_one(self) -> 'AIPipelinesBuilder':
        ''' Retrieve one of the pipelines '''
        identifier = self._get_identifier()
        self.requires = {
            'organization': self.organization_name,
            'identifier': identifier
        }
        self.url = f'{self.client.url}/north/ai/{self.organization_name}/pipelines/{identifier}'
        self.method = 'find_one'
        return self

    def update(self) -> 'AIPipelinesBuilder':
        ''' Update a model and have the option to incorporate the with_config_file function, 
            to modify its pipeline_id in the configuration file '''
        identifier = self._get_identifier()
        self.requires = {
            'organization_name': self.organization_name,
            'identifier': identifier,
            'name': self.name
        }

        self.url = f'{self.client.url}/north/ai/{self.organization_name}/pipelines/{identifier}'
        self.method = 'update'
        return self

    def delete(self) -> 'AIPipelinesBuilder':
        ''' Delete model '''
        identifier = self._get_identifier()
        self.requires = {
            'organization': self.organization_name,
            'identifier': identifier
        }

        self.url = f'{self.client.url}/north/ai/{self.organization_name}/pipelines/{identifier}'
        self.method = 'delete'
        return self

    def prediction(self) -> 'AIPipelinesBuilder':
        ''' Prediction model '''
        identifier = self._get_identifier()
        self.requires = {
            'organization': self.organization_name,
            'identifier': identifier,
            'prediction': self.data_prediction
        }
        self.url = f'{self.client.url}/north/ai/{self.organization_name}/pipelines/{identifier}/prediction'
        self.method = 'prediction'
        return self
    
    def save(self) -> 'AIPipelinesBuilder':
        ''' Create or update model '''
        self.requires = {
            'organization': self.organization_name,
        }
        self.method = 'save'
        return self

    def set_config_file_identifier(self) -> 'AIPipelinesBuilder':
        ''' Set model id in config file '''
        self.requires = {
            'identifier': self.identifier,
            'config file': self.config_file,
            'self.section': self.section,
            'self.config_key': self.config_key
        }
        self.method = 'set_config_identifier'
        return self
    
    def set_env_identifier(self) -> 'AIPipelinesBuilder':
        ''' set model id in env '''
        self.requires = {
            'identifier': self.identifier,
            'env': self.data_env
        }
        self.method = 'set_env_identifier'
        return self

    def build(self) -> 'AIPipelinesBuilder':
        ''' Check if any parameter is missing. '''
        # Se necesita comprobar que son solo los que deben de aparecer no todos!!!
        for key, value in self.requires.items():
            assert value is not None, f'{key} is required'
        return self
        
    def execute(self):
        ''' Execute and return the responses '''
        methods = {
            'create': self._execute_create,
            'find_one': self._execute_find_one,
            'find_all': self._execute_find_all,
            'update': self._execute_update,
            'delete': self._execute_delete,
            'prediction': self._execute_prediction,
            'save': self._execute_save,
            'set_config_identifier': self._execute_set_identifier,
            'set_env_identifier': self._execute_env_identifier,
        }

        function = methods.get(self.method)
        if function is None:
            raise ValueError(f'Unsupported method: {self.method}')
        return function()

    def _execute_create(self):
        name = self.name  
        actions = self.actions

        if not name:
            raise ValueError('The "with_name" is required.')

        if not actions:
            raise ValueError('The "add_action is required.')
        
        data = {
            "name": name,
            "actions": actions
        }

        response = requests.post(self.url, headers=self.client.headers, json=data, verify=False, timeout = 3000)
        if response.status_code != 201:
            raise ValueError(response.text)
        
        if response.status_code == 201:
            file_config = self._read_config_file()
            all_identifiers = self.find_all().build().execute().json()
            for item in all_identifiers:
                if item['name'] == name:
                    result = item['identifier']
                    break

            if file_config:
                try:
                    file_config.get(self.section, self.config_key)
                    file_config.set(self.section, self.config_key, result)
                    with open(self.config_file, 'w', encoding='utf-8') as configfile:
                        file_config.write(configfile)

                except configparser.NoOptionError as error:
                    raise ValueError('The "pipeline_id" parameter was not found in the configuration file.') from error

            elif self.data_env is not None:
                try:
                    env_vars = dotenv_values('.env')
                    if self.data_env not in env_vars:
                        raise KeyError('The environment variable was not found in the .env file.')
                    
                    set_key('.env', self.data_env, result)

                except KeyError as error:
                    raise ValueError('The environment variable was not found in the .env file.') from error

            return response

    def _execute_find_one(self) -> Union[requests.Response, List[Dict[str, Any]]]:
        response = requests.get(self.url, headers=self.client.headers, verify=False, timeout = 3000)
        return response
    
    def _execute_find_all(self) -> Union[requests.Response, List[Dict[str, Any]]]:
        response = requests.get(self.url, headers=self.client.headers, verify=False, timeout=3000)
        return response
    
    def _execute_update(self):
        name = self.name  
        actions = self.actions
        
        data = {
        "name": name,
        "actions": actions
        }

        response = requests.put(self.url, headers=self.client.headers, json=data, verify=False, timeout = 3000)

        if response.status_code != 200:
            raise ValueError(response.text)
        
        return response
        
    def _execute_delete(self):
        response = requests.delete(self.url, headers=self.client.headers, verify=False, timeout = 3000)
        return response
            
    def _execute_prediction(self):
        self.client.headers['Content-Type'] = 'application/json'
        prediction = {
            'input': json.dumps(self.data_prediction),
            'collect': self.collect
        }
        response = requests.post(self.url, headers=self.client.headers, data=prediction,  verify=False, timeout = 3000)
        return response

    def _execute_save(self) -> Union[requests.Response, int]:
        if self.data_env is not None or self.config_file is not None:
            if self.data_env is not None:
                identifier = dotenv_values('.env')[self.data_env]
                self.identifier = identifier
                
            elif self.config_file is not None:
                config = configparser.ConfigParser()
                config.read(self.config_file)
                pipeline_id = config.get(self.section, self.config_key, fallback=None)
                self.identifier = pipeline_id

            response = self.find_one().build().execute()
            if response.status_code == 200:
                #Update
                return self.update().build().execute()
            # Create
            return self.create().build().execute()
        
        return ValueError('The "config file" or env parameter was not found')  
        
    def _execute_set_identifier(self):
        try:
            file_config = self._read_config_file()
            self._read_config_file().get(self.section, self.config_key)
            file_config.set(self.section, self.config_key, self.identifier)
            with open(self.config_file, 'w', encoding='utf-8') as configfile:
                file_config.write(configfile)
            return None
        
        except configparser.NoOptionError:
            return ValueError('The "pipeline_id" parameter was not found in the configuration file.')

    def _execute_env_identifier(self) -> None:
        try:
            env_vars = dotenv_values('.env')
            if self.data_env not in env_vars:
                raise KeyError('The environment variable was not found in the .env file.')
                    
            set_key('.env', self.data_env, self.identifier)

        except KeyError as error:
            raise ValueError('The environment variable was not found in the .env file.') from error


    def _read_config_file(self):
        if self.config_file is not None:
            if os.path.exists(self.config_file):
                config = configparser.ConfigParser()
                config.read(self.config_file)
                return config
            raise ValueError('The configuration file does not exist.')
        return None
    