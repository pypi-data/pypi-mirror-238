'''  AITransformersBuilder '''
import json
import os
import configparser
import mimetypes
from  typing import Any, Dict, List, Tuple, Optional, Union
from dotenv import load_dotenv, dotenv_values, set_key
import requests

class AITransformersBuilder:
    ''' Class transformer builder '''
    def __init__(self, opengate_client: str) -> None:
        self.client: str = opengate_client
        self.organization_name: str = None
        self.identifier: str = None
        self.config_file: str = None
        self.data_env: str = None
        self.section: str = None
        self.config_key: str = None
        self. data_evaluate: Dict = {}
        self.url: str = None
        self.requires: Dict = {}
        self.method: str = None
        self.name: str = None
        self.find_name: str = None
        self.output_file_path: str = None
        self.file_name: str = None
        self.files: List[Tuple[str, str]] = []

    def with_organization(self, organization_name: str) -> 'AITransformersBuilder':
        ''' User organization '''
        self.organization_name = organization_name
        return self
    
    def with_identifier(self, identifier: str) -> 'AITransformersBuilder':
        ''' Transformer Identifier '''
        self.identifier = identifier
        return self
    
    def with_config_file(self, config_file: str) -> 'AITransformersBuilder':
        ''' Path along with the configuration file name. '''
        self.config_file = config_file
        return self
    
    def with_env(self, data_env: str) -> 'AITransformersBuilder':
        ''' env '''
        self.data_env = data_env
        return self
    
    def add_file(self, file_path: str, filetype: str = None):
        ''' add file '''
        if not os.path.isabs(file_path):
            file_path = os.path.join(os.getcwd(), file_path)

        if filetype is None:
            filetype = self._get_file_type(file_path)

        self.files.append((file_path, filetype))
        return self

    def _get_file_type(self, file_path: str) -> str:
        filename = os.path.basename(file_path)
        type_guess = mimetypes.guess_type(filename)[0]

        if filename.endswith('.py'):
            return 'text/python'

        return type_guess if type_guess else 'application/octet-stream'

    def with_find_by_name(self, find_name: str) -> 'AITransformersBuilder':
        ''' Find transformer by name'''
        self.find_name = find_name
        return self
    
    def with_evaluate(self,data_evaluate: dict) -> 'AITransformersBuilder':
        ''' evaluate data '''
        self. data_evaluate = data_evaluate
        return self
    
    def with_output_file_path(self, output_file_path: str) -> 'AITransformersBuilder':
        ''' output_file_download '''
        self.output_file_path = output_file_path
        return self
    
    def with_file_name(self, file_name: str) -> 'AITransformersBuilder':
        ''' file_name '''
        self.file_name = file_name
        return self
    
    def create(self) -> 'AITransformersBuilder':
        '''Create a transformer and have the option to incorporate the with_config_file function, 
            to modify its transformer_id in the configuration file'''
        self.requires = {
            'organization': self.organization_name
        }
        self.url = f'{self.client.url}/north/ai/{self.organization_name}/transformers'
        self.method = 'create'
        return self

    def find_all(self) -> 'AITransformersBuilder':
        ''' Retrieve all the transformers.'''
        self.requires = {
            'organization': self.organization_name
        }
        self.url = f'{self.client.url}/north/ai/{self.organization_name}/transformers'
        self.method = 'find_all'
        return self

    def _get_identifier(self) -> str:
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
                return self._read_config_file().get(self.section, self.config_key)
            except configparser.NoOptionError:
                return ValueError('The "transformer_id" parameter was not found in the configuration file.')

        if self.find_name is not None:
            all_identifiers = self.find_all().build().execute().json()
            name_identifier = [item['identifier'] for item in all_identifiers if item['name'] == self.find_name]

            if not name_identifier:
                raise ValueError('File name does not exist')

            return name_identifier[0]
        
        raise ValueError('A configuration file with identifier, a model identifier or a find by name is required.')
    
    def find_one(self) -> 'AITransformersBuilder':
        ''' Retrieve one the transformers.'''
        
        identifier = self._get_identifier()
        self.requires = {
            'organization': self.organization_name,
            'identifier': identifier
        }
        self.url = f'{self.client.url}/north/ai/{self.organization_name}/transformers/{identifier}'
        self.method = 'find_one'
        return self

    def update(self) -> 'AITransformersBuilder':
        '''
        Update a model and have the option to incorporate the with_config_file function, 
            to modify its transformer_id in the configuration file 
        '''
        identifier = self._get_identifier()
        self.requires = {
            'organization': self.organization_name,
            'identifier': identifier
        }

        self.url = f'{self.client.url}/north/ai/{self.organization_name}/transformers/{identifier}'
        self.method = 'update'
        return self

    def delete(self) -> 'AITransformersBuilder':
        ''' Delete model '''
        identifier = self._get_identifier()
        self.requires = {
            'organization': self.organization_name
        }

        self.url = f'{self.client.url}/north/ai/{self.organization_name}/transformers/{identifier}'
        self.method = 'delete'
        return self

    def download(self) -> 'AITransformersBuilder':
        ''' Get model identifier'''
        identifier = self._get_identifier()
        self.requires = {
            'organization': self.organization_name,
            'identifier': identifier,
            'output_file': self.output_file_path,
            'file_name': self.file_name
        }

        self.url = f'{self.client.url}/north/ai/{self.organization_name}/transformers/{identifier}/{self.file_name}'
        self.method = 'download'
        return self

    def evaluate(self) -> 'AITransformersBuilder':
        ''' evaluate model'''
        identifier = self._get_identifier()
        self.requires = {
            'organization': self.organization_name,
            'identifier': identifier,
            'evaluate': self.data_evaluate
        }
        self.url = f'{self.client.url}/north/ai/{self.organization_name}/transformers/{identifier}/transform'
        self.method = 'evaluate'
        return self
    
    def save(self) -> 'AITransformersBuilder':
        ''' Create or update model'''
        self.requires = {
            'organization': self.organization_name,
        }
        self.method = 'save'
        return self

    def set_config_file_identifier(self) -> 'AITransformersBuilder':
        ''' set model id in config file '''
        self.requires = {
            'identifier': self.identifier,
            'config_file': self.config_file
        }
        self.method = 'set_config_identifier'
        return self
    
    def set_env_identifier(self) -> 'AITransformersBuilder':
        ''' set model id in env '''
        self.requires = {
            'identifier': self.identifier,
            'env': self.data_env
        }
        self.method = 'set_env_identifier'
        return self

    def build(self):
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
            'download': self._execute_download,
            'evaluate': self._execute_evaluate,
            'save': self._execute_save,
            'set_config_identifier': self._execute_set_identifier,
            'set_env_identifier': self._execute_env_identifier,
        }

        function = methods.get(self.method)
        if function is None:
            raise ValueError(f'Unsupported method: {self.method}')
        return function()

    def _execute_create(self) -> requests.Response:
        file_config: Optional[configparser.ConfigParser] = self._read_config_file()
        files_to_upload = self._prepare_files(self.files)
        response: requests.Response = requests.post(self.url, headers=self.client.headers, data={}, files=files_to_upload, verify=False, timeout=3000)
        if response.status_code == 201:
            all_identifiers: Dict = self.find_all().build().execute().json()
            python_files: List[str] = [filename for filename, filetype in self.files if filetype == 'text/python']
            python_file = python_files[0]
            filename = os.path.basename(python_file)
            result = next((item for item in all_identifiers if item['name'] == filename), None)
            if result is not None:
                if file_config:
                    try:
                        self._read_config_file().get(self.section, self.config_key)
                        file_config.set(self.section, self.config_key, result['identifier'])
                        with open(self.config_file, 'w', encoding='utf-8') as configfile:
                            file_config.write(configfile)
                    except configparser.NoOptionError as error:
                        raise ValueError('The "transformer_id" parameter was not found in the configuration file.') from error
            elif self.data_env is not None:
                try:
                    env_vars = dotenv_values('.env')
                    if self.data_env not in env_vars:
                        raise KeyError('The environment variable was not found in the .env file.')
                    
                    set_key('.env', self.data_env, result['identifier'])

                except KeyError as error:
                    raise ValueError('The environment variable was not found in the .env file.') from error
                
        return response
    
    def _execute_find_all(self) -> requests.Response:
        response: requests.Response = requests.get(self.url, headers=self.client.headers, verify=False, timeout=3000)
        return response

    def _execute_find_one(self) -> requests.Response:
        response: requests.Response = requests.get(self.url, headers=self.client.headers, verify=False, timeout=3000)
        return response
            
    def _execute_update(self) -> requests.Response:
        files_to_upload = self._prepare_files(self.files)
        response: requests.Response = requests.put(self.url, headers=self.client.headers, data={}, files=files_to_upload, verify=False, timeout=3000)
        response.raise_for_status()
        return response
    
    def _execute_delete(self) -> int:
        response: requests.Response = requests.delete(self.url, headers=self.client.headers, verify=False, timeout=3000)
        return response
     
    def _execute_download(self) -> int:
        response: requests.Response = requests.get(self.url, stream=True, headers=self.client.headers, verify=False, timeout=3000)
        if response.status_code == 200:
            with open(self.output_file_path , 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        else:
            raise ValueError('Failed to download the file. Status code:', response.status_code)
        return response
        
    def _execute_evaluate(self) -> Union[int, Dict]:
        self.client.headers['Content-Type'] = 'application/json'
        response: requests.Response = requests.post(self.url, headers=self.client.headers, data=json.dumps(self.data_evaluate), verify=False, timeout=3000)
        return response
    def _validate_response(self, response: requests.Response) -> Any:
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()
        raise response.status_code

    def _execute_evaluate(self) -> Union[int, Dict]:
        self.client.headers['Content-Type'] = 'application/json'
        response: requests.Response = requests.post(self.url, headers=self.client.headers, data=json.dumps(self.data_evaluate), verify=False, timeout=3000)
        return self._validate_response(response)

    def _execute_save(self) -> Union[requests.Response, int]:
        if self.data_env is not None or self.config_file is not None:
            if self.data_env is not None:
                identifier = dotenv_values('.env')[self.data_env]
                self.identifier = identifier

            elif self.config_file is not None:
                config = configparser.ConfigParser()
                config.read(self.config_file)
                transformer_id = config.get(self.section, self.config_key, fallback=None)
                self.identifier = transformer_id

            response = self.find_one().build().execute()
            if response.status_code == 200:
                #Update
                return self.update().build().execute()
            # Create
            return self.create().build().execute()
        
        return ValueError('The "config file" or env parameter was not found')
        
    def _execute_set_identifier(self) -> Optional[Union[None, ValueError]]:
        try:
            file_config: Optional[configparser.ConfigParser] = self._read_config_file()
            self._read_config_file().get('id', 'transformer_id')
            file_config.set('id', 'transformer_id', self.identifier)
            with open(self.config_file, 'w', encoding='utf-8') as configfile:
                file_config.write(configfile)
            return None
        except configparser.NoOptionError:
            return ValueError('The "transformer_id" parameter was not found in the configuration file.')

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
                config: configparser.ConfigParser = configparser.ConfigParser()
                config.read(self.config_file)
                return config
            raise ValueError('The configuration file does not exist.')
        return None

    def _prepare_files(self, files: List[Tuple]) -> List[Tuple[str, Tuple[str, bytes, str]]]:
        files_to_upload: List[Tuple[str, Tuple[str, bytes, str]]] = []
        for file_obj in files:
            file_path, file_type = file_obj
            with open(file_path, 'rb') as file:
                file_data = file.read()
            file_entry: Tuple[str, Tuple[str, bytes, str]] = ('files', (os.path.basename(file_path), file_data, file_type))
            files_to_upload.append(file_entry)
        return files_to_upload
    