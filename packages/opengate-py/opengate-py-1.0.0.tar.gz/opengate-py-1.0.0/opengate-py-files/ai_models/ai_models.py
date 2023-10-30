'''  AIModelsBuilder '''
import json
import os
import configparser
import requests
import urllib3
from dotenv import load_dotenv, set_key, dotenv_values
from  typing import Any, Dict, List, Tuple, Optional, Union


class AIModelsBuilder:
    ''' Class model builder'''
    def __init__(self, opengate_client: str):
        self.client: str = opengate_client
        self.organization_name: str = None
        self.identifier: str = None
        self.config_file: str = None
        self.section: str = None
        self.config_key: str = None
        self.data_env: str = None
        self.file_name: str = None
        self.new_file: None = None
        self.data_prediction: None = None
        self.url: str = None
        self.requires: Dict[str, str] = None
        self.method: str = None
        self.name: str = None
        self.find_name: str = None
        self.output_file_path: str = None
        self.full_file_path: str = None 

    def with_organization(self, organization_name: str) -> 'AIModelsBuilder':
        ''' organization '''
        self.organization_name = organization_name
        return self
    
    def with_identifier(self, identifier: str) -> 'AIModelsBuilder':
        ''' identifier '''
        self.identifier = identifier
        return self
    
    def with_config_file(self,config_file: str, section: str, config_key: str) -> 'AIModelsBuilder':
        ''' config file. '''
        self.config_file = config_file
        self.section = section
        self.config_key = config_key
        return self
    
    def with_env(self, data_env: str) -> 'AIModelsBuilder':
        ''' env '''
        self.data_env = data_env
        return self
    
    def add_file(self, file: str) -> 'AIModelsBuilder':
        ''' Add a file with its path '''
        self.file_name = os.path.basename(file)
        self.full_file_path = os.path.abspath(file)
        return self
    
    def with_find_by_name(self, find_name: str) -> 'AIModelsBuilder':
        ''' Find model by name'''
        self.find_name = find_name
        return self
    
    def with_prediction(self, data_prediction: dict) -> 'AIModelsBuilder':
        ''' Prediction data '''
        self.data_prediction = data_prediction
        return self
    
    def with_output_file_path(self, output_file_path: str) -> 'AIModelsBuilder':
        ''' output file path'''
        self.output_file_path = output_file_path
        return self
    
    def create(self) -> 'AIModelsBuilder':
        '''Create a model and have the option to incorporate the with_config_file function, 
            to modify its model_id in the configuration file'''
        self.requires = {
            'organization_name': self.organization_name, 
            'add_file': self.file_name
        }
        self.url = f'{self.client.url}/north/ai/{self.organization_name}/models'
        self.method = 'create'
        return self

    def find_all(self) -> 'AIModelsBuilder':
        ''' Retrieve all the models.'''
        self.requires = {
            'organization_name': self.organization_name
        }
        self.url = f'{self.client.url}/north/ai/{self.organization_name}/models'
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

        elif self.config_file is not None and self.section is not None and self.config_key is not None :
            try:
                config = configparser.ConfigParser()
                config.read(self.config_file)
                return config.get(self.section, self.config_key)
            except (configparser.NoOptionError, configparser.NoSectionError):
                raise ValueError('The "model_id" parameter was not found in the configuration file.')

        elif self.find_name is not None:
            all_identifiers = self.find_all().build().execute().json()
            name_identifier = [item['identifier'] for item in all_identifiers if item['name'] == self.find_name]

            if not name_identifier:
                raise ValueError('File name does not exist')

            return name_identifier[0]

        raise ValueError('A configuration file with identifier, a model identifier, or a find by name is required.')
    
    def find_one(self) -> 'AIModelsBuilder':
        ''' Retrieve one the models.'''
        
        identifier = self._get_identifier()
        self.requires = {
            'organization_name': self.organization_name,
            'identifier': identifier
        }
        self.url = f'{self.client.url}/north/ai/{self.organization_name}/models/{identifier}'
        self.method = 'find_one'
        return self

    def update(self) -> 'AIModelsBuilder':
        '''
        Update a model and have the option to incorporate the with_config_file function, 
            to modify its model_id in the configuration file 
        '''
        identifier = self._get_identifier()
        self.requires = {
            'organization_name': self.organization_name,
            'identifier': identifier
        }

        self.url = f'{self.client.url}/north/ai/{self.organization_name}/models/{identifier}'
        self.method = 'update'
        return self

    def delete(self) -> 'AIModelsBuilder':
        ''' Delete model '''
        identifier = self._get_identifier()
        self.requires = {
            'organization_name': self.organization_name,
            'identifier': identifier
        }

        self.url = f'{self.client.url}/north/ai/{self.organization_name}/models/{identifier}'
        self.method = 'delete'
        return self

    def validate(self) -> 'AIModelsBuilder':
        ''' validate '''
        self.requires = {
            'organization_name': self.organization_name,
            'add_file': self.file_name
        }
        self.url = f'{self.client.url}/north/ai/{self.organization_name}/models/validate'
        self.method = 'validate'
        return self

    def download(self) -> 'AIModelsBuilder':
        ''' Get model identifier'''
        identifier = self._get_identifier()
        self.requires = {
            'organization_name': self.organization_name,
            'identifier': identifier,
            'output_file': self.output_file_path
        }

        self.url = f'{self.client.url}/north/ai/{self.organization_name}/models/{identifier}/file'
        self.method = 'download'
        return self

    def prediction(self) -> 'AIModelsBuilder':
        ''' prediction model'''
        identifier = self._get_identifier()
        self.requires = {
            'organization_name': self.organization_name,
            'identifier': identifier,
            'prediction': self.data_prediction
        }
        self.url = f'{self.client.url}/north/ai/{self.organization_name}/models/{identifier}/prediction'
        self.method = 'prediction'
        return self
    
    def save(self) -> 'AIModelsBuilder':
        ''' Create or update model'''
        self.requires = {
            'organization': self.organization_name,
        }
        self.method = 'save'
        return self

    def set_config_file_identifier(self) -> 'AIModelsBuilder':
        ''' set model id in config file '''
        self.requires = {
            'identifier': self.identifier,
            'config_file': self.config_file,
            'self.section': self.section,
            'self.config_key': self.config_key
        }
        self.method = 'set_config_file_identifier'
        return self
    
    def set_env_identifier(self) -> 'AIModelsBuilder':
        ''' set model id in env '''
        self.requires = {
            'identifier': self.identifier,
            'env': self.data_env
        }
        self.method = 'set_env_identifier'
        return self

    def build(self) -> 'AIModelsBuilder':
        ''' Check if any parameter is missing. '''
        # Se necesita comprobar que son solo los que deben de aparecer no todos!!!
        for key, value in self.requires.items():
            assert value is not None, f'{key} is required'
        return self
        
    def execute(self) -> requests.Response:
        ''' Execute and return the responses '''
        methods = {
            'create': self._execute_create,
            'find_all': self._execute_find_all,
            'find_one': self._execute_find_one,
            'update': self._execute_update,
            'delete': self._execute_delete,
            'validate': self._execute_validate,
            'download': self._execute_download,
            'prediction': self._execute_prediction,
            'save': self._execute_save,
            'set_config_file_identifier': self._execute_set_identifier,
            'set_env_identifier': self._execute_env_identifier,
        }
        
        function = methods.get(self.method)
        if function is None:
            raise ValueError(f'Unsupported method: {self.method}')
        return function()

    def _execute_create(self) -> requests.Response:
        file_config: Optional[configparser.ConfigParser] = None
        files = self._get_file_data()
        payload: Dict[str, Any] = {}
        file_config = self._read_config_file()
        response = requests.post(self.url, headers=self.client.headers, data=payload, files=files, verify=False, timeout=3000)
        if response.status_code == 201:
            all_identifiers = self.find_all().build().execute().json()
            identifiers = [item['identifier'] for item in all_identifiers if item['name'] == self.file_name]
            if file_config:
                try:
                    self._read_config_file().get(self.section, self.config_key)
                    file_config.set(self.section, self.config_key, identifiers[0])
                    with open(self.config_file, 'w', encoding='utf-8') as configfile:
                        file_config.write(configfile)

                except configparser.NoOptionError:
                    return ValueError('The "model_id" parameter was not found in the configuration file.')
            elif self.data_env is not None:
                try:
                    env_vars = dotenv_values('.env')
                    if self.data_env not in env_vars:
                        raise KeyError('The environment variable was not found in the .env file.')
                    
                    set_key('.env', self.data_env, identifiers[0])

                except KeyError as error:
                    raise ValueError('The environment variable was not found in the .env file.') from error

        return response

    def _execute_find_all(self) -> Union[requests.Response, List[Dict[str, Any]]]:
        response = requests.get(self.url, headers=self.client.headers, verify=False, timeout=3000)
        return response

    def _execute_find_one(self) -> Union[requests.Response, Dict[str, Any]]:
        response = requests.get(self.url, headers=self.client.headers, verify=False, timeout=3000)
        return response
    
    def _execute_update(self) -> requests.Response:
        files = self._get_file_data()
        payload: Dict[str, Any] = {}
        response = requests.put(self.url, headers=self.client.headers, data=payload, files=files, verify=False, timeout=3000)
        return response
    
    def _execute_delete(self) -> int:
        response = requests.delete(self.url, headers=self.client.headers, verify=False, timeout=3000)
        return response
    
    def _execute_validate(self) -> Union[requests.Response, Dict[str, Any]]:
        files = self._get_file_data()
        payload: Dict[str, Any] = {}
        response = requests.post(self.url, headers=self.client.headers, data=payload, files=files, verify=False, timeout=3000)
        return response
        
    def _execute_download(self) -> int:
        response = requests.get(self.url, stream=True, headers=self.client.headers, verify=False, timeout=3000)
        if response.status_code == 200:
            with open(self.output_file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        else:
            raise ValueError('Failed to download the file. Status code:', response.status_code)
        return response.status_code

    def _execute_prediction(self) -> Union[requests.Response, Dict[str, Any]]:
        self.client.headers['Content-Type'] = 'application/json'
        response = requests.post(self.url, headers=self.client.headers, data=json.dumps(self.data_prediction), verify=False, timeout=3000)
        return response

    def _execute_save(self) -> Union[requests.Response, int]:
        if self.data_env is not None or self.config_file is not None:
            if self.data_env is not None:
                identifier = dotenv_values('.env')[self.data_env]
                self.identifier = identifier
                
            elif self.config_file is not None:
                config = configparser.ConfigParser()
                config.read(self.config_file)
                model_id = config.get(self.section, self.config_key, fallback=None)
                self.identifier = model_id
 
            response = self.find_one().build().execute()
            if response.status_code == 200:
                #Update
                return self.update().build().execute()
            # Create
            return self.create().build().execute()
        
        return ValueError('The "config file" or env parameter was not found')
        
    def _execute_set_identifier(self) -> None:
        try:
            file_config = self._read_config_file()
            self._read_config_file().get(self.section, self.config_key)
            file_config.set(self.section, self.config_key, self.identifier)
            with open(self.config_file, 'w', encoding='utf-8') as configfile:
                file_config.write(configfile)
            
        except configparser.NoOptionError as error:
            raise ValueError('The "model_id" parameter was not found in the configuration file.') from error
    
    def _execute_env_identifier(self) -> None:
        try:
            env_vars = dotenv_values('.env')
            if self.data_env not in env_vars:
                raise KeyError('The environment variable was not found in the .env file.')
                    
            set_key('.env', self.data_env, self.identifier)

        except KeyError as error:
            raise ValueError('The environment variable was not found in the .env file.') from error

    def _read_config_file(self) -> Optional[configparser.ConfigParser]:
        if self.config_file is not None:
            if os.path.exists(self.config_file):
                config = configparser.ConfigParser()
                config.read(self.config_file)
                return config
            raise ValueError('The configuration file does not exist.')
        return None
    
    def _get_file_data(self):
        with open(self.full_file_path, 'rb') as file:
            file_data = file.read()
        files = [('modelFile', (self.file_name, file_data, 'application/octet-stream'))]
        return files
    