'''  RulesBuilder '''
import requests
import os
import configparser
import json
import urllib3
import re
from dotenv import load_dotenv, set_key, dotenv_values
from typing import Callable, Union, List, Dict, Any

class RulesBuilder:
    ''' Class rules builder'''
    def __init__(self, opengate_client):
        self.client = opengate_client
        self.rule_data: Dict[str, Any] = {}
        self.method: str = None
        self.url: str = None
        self.filter_data: Dict[str, Any] = None
        self.requires: Dict[str, Any] = {}
        self.config_file: str = None
        self.section: str = None
        self.config_key: str = None
        self.find_name: str = None
        self.data_env: str = None
    
    def with_actions(self, actions: Dict[str, Any]) -> 'RulesBuilder':
        '''Actions'''
        self.rule_data['actions'] = actions
        return self

    def with_actions_delay(self, actions_delay: int) -> 'RulesBuilder':
        '''Actions Delay'''
        self.rule_data['actionsDelay'] = actions_delay
        return self

    def with_active(self, active: bool) -> 'RulesBuilder':
        '''Active'''
        self.rule_data['active'] = active
        return self

    def with_channel(self, channel: str) -> 'RulesBuilder':
        '''Channel'''
        self.rule_data['channel'] = channel
        return self

    def with_condition(self, condition: Dict[str, Any]) -> 'RulesBuilder':
        '''Condition'''
        self.rule_data['condition'] = condition
        return self

    def with_identifier(self, identifier: str) -> 'RulesBuilder':
        '''Identifier'''
        self.rule_data['identifier'] = identifier
        return self

    def with_mode(self, mode: str) -> 'RulesBuilder':
        '''Mode'''
        if mode in {"EASY", "ADVANCED"}:
            self.rule_data['mode'] = mode
        else:
            raise ValueError('It is necessary to introduce a type of rule "EASY" or "ADVANCED"')
                
        return self

    def with_name(self, name: str) -> 'RulesBuilder':
        '''Name'''
        self.rule_data['name'] = name
        return self

    def with_organization(self, organization: str) -> 'RulesBuilder':
        '''Organization'''
        self.rule_data['organization'] = organization
        return self
    
    def with_description(self, description: str) -> 'RulesBuilder':
        '''Description'''
        self.rule_data['description'] = description
        return self
    
    def with_type(self, rule_type: Dict[str, Any]) -> 'RulesBuilder':
        '''Type'''
        self.rule_data['type'] = rule_type
        return self
    
    def with_parameters(self, parameters: Dict[str, str]) -> 'RulesBuilder':
        '''Parameters'''
        self.rule_data['parameters'] = parameters
        return self
    
    def with_code(self, code: str) -> 'RulesBuilder':
        '''javascript code in'''
        if self.rule_data['mode'] is not None and self.rule_data['mode'] == "ADVANCED":
            self.rule_data['javascript'] = self._convert_to_one_line(code)
        else:
            raise ValueError('It is necessary to introduce a mode of rule and that it be advanced')
        return self
    
    def with_code_file(self, code_file: str) -> 'RulesBuilder':
        '''Type'''
        if self.rule_data['mode'] is not None and self.rule_data['mode'] == "ADVANCED":
            if os.path.exists(code_file):
                if os.path.isfile(code_file):
                    with open(code_file, 'r', encoding="utf-8") as file:
                        code_file = file.read()
                        self.rule_data['javascript'] = self._convert_to_one_line(code_file)
            else:
                raise ValueError(f"{code_file} is not a valid file")
        else:
            raise ValueError('It is necessary to introduce a mode EASY or ADVANCED')
        return self

    def with_env(self, data_env: str) -> 'RulesBuilder':
        ''' env '''
        self.data_env = data_env
        return self

    def with_filter(self, filter_data: Dict[str, Any]) -> 'RulesBuilder':
        '''filter'''
        self.filter_data = filter_data
        return self
    
    def with_config_file(self,config_file: str, section: str, config_key: str) -> 'RulesBuilder':
        ''' config file. '''
        self.config_file = config_file
        self.section = section
        self.config_key = config_key
        return self
    
    def with_find_by_name(self, find_name:str) -> 'RulesBuilder':
        ''' Find rule by name'''
        self.find_name = find_name
        return self
    
    def create(self) -> 'RulesBuilder':
        ''' create '''
        self.requires = {
            'organization': self.rule_data["organization"],
            'name': self.rule_data['name'],
            'mode': self.rule_data["mode"],
            'action delay': self.rule_data['actionsDelay'],
            'channel': self.rule_data["channel"],
        }
        self.url = f'{self.client.url}/north/v80/rules/provision/organizations/{self.rule_data["organization"]}/channels/{self.rule_data["channel"]}'
        self.method = 'create'
        return self

    def search(self) -> 'RulesBuilder':
        ''' search '''
        self.requires = {
            'filter': self.filter_data,
        }
        self.requires['filter'] = self.filter_data
        self.url = f'{self.client.url}/north/v80/rules/search'
        self.method = 'search'
        return self
    
    def find_one(self) -> 'RulesBuilder':
        '''Find one '''
        identifier = self._get_identifier()
        self.requires = {
            'organization': self.rule_data["organization"], 
            'channel': self.rule_data["channel"],
            'identifier': identifier,
        }
        self.url = f'{self.client.url}/north/v80/rules/provision/organizations/{self.rule_data["organization"]}/channels/{self.rule_data["channel"]}/{identifier}'
        self.method = 'find_one'
        return self
    
    def update(self) -> 'RulesBuilder':
        ''' Update'''
        identifier = self._get_identifier()
        self.requires = {
            'organization': self.rule_data["organization"],
            'name': self.rule_data['name'],
            'mode': self.rule_data["mode"],
            'action delay': self.rule_data['actionsDelay'],
            'channel': self.rule_data["channel"],
            'identifier': identifier,
        }
        identifier = self._get_identifier()
        self.url = f'{self.client.url}/north/v80/rules/provision/organizations/{self.rule_data["organization"]}/channels/{self.rule_data["channel"]}/{identifier}'
        self.method = 'update'
        return self
    
    def delete(self) -> 'RulesBuilder':
        ''' Deleete '''
        identifier = self._get_identifier()
        self.requires = {
            'organization': self.rule_data["organization"], 
            'channel': self.rule_data["channel"],
            'identifier': identifier,
        }
        self.url = f'{self.client.url}/north/v80/rules/provision/organizations/{self.rule_data["organization"]}/channels/{self.rule_data["channel"]}/{identifier}'
        self.method = 'delete'
        return self
    
    def update_parameters(self) -> 'RulesBuilder':
        ''' Update parameters '''
        identifier = self._get_identifier()
        self.requires = {
            'organization': self.rule_data["organization"], 
            'channel': self.rule_data["channel"],
            'identifier': identifier,
            'parameters': self.rule_data["parameters"]
        }
        self.url = f'{self.client.url}/north/v80/rules/provision/organizations/{self.rule_data["organization"]}/channels/{self.rule_data["channel"]}/{identifier}/parameters'
        self.method = 'update_parameters'
        return self
    
    def catalog(self) -> 'RulesBuilder':
        ''' catalog '''
        self.url = f'{self.client.url}/north/v80/rules/catalog'
        self.method = 'catalog'
        return self
    
    def save(self) -> 'RulesBuilder':
        ''' Create or update model '''
        self.requires = {
            'organization': self.rule_data["organization"]
        }
        self.method = 'save'
        return self
    
    def set_config_file_identifier(self) -> 'RulesBuilder':
        ''' Set model id in config file '''
        identifier = self._get_identifier()
        self.requires = {
            'identitifer': identifier,
            'config file': self.config_file,
            'self.section': self.section,
            'self.config_key': self.config_key
        }
        self.method = 'set_config_identifier'
        return self

    def set_env_identifier(self) -> 'RulesBuilder':
        ''' set model id in env '''
        self.requires = {
            'identifier': self.identifier,
            'env': self.data_env
        }
        self.method = 'set_env_identifier'
        return self

    def build(self) -> 'RulesBuilder':
        ''' Builder and check if any parameter is missing. '''
        if self.requires is not None:
            for key, value in self.requires.items():
                assert value is not None, f'{key} is required'
        return self

    def execute(self) -> Union[int, List[Dict[str, Any]]]:
        ''' Execute and return the responses '''

        methods: Dict[str, Callable[[], Union[int, List[Dict[str, Any]]]]] = {
            'create': self._execute_create,
            'search': self._execute_search,
            'find_one': self._execute_find_one,
            'update': self._execute_update,
            'delete': self._execute_delete,
            'update_parameters': self._execute_update_parameters,
            'catalog': self._execute_catalog,
            'save': self._execute_save,
            'set_config_identifier': self._execute_set_identifier
        }

        function = methods.get(self.method)
        if function is None:
            raise ValueError(f'Unsupported method: {self.method}')
        return function()

    def _convert_to_one_line(self, input_code: str) -> str:
        """ Convert a multi-line code into a single line """
        comments: List[str] = re.findall(r'\/\/.*|\/\*[\s\S]*?\*\/', input_code)
        input_code: str = re.sub(r'\/\/.*', '', input_code)
        input_code: str = re.sub(r'\/\*[\s\S]*?\*\/', '', input_code)
        one_line_code: str = re.sub(r'\n', ' ', input_code)
        one_line_code: str = re.sub(r'\s+', ' ', one_line_code)
        one_line_code: str = one_line_code.strip()

        for comment in comments:
            one_line_code = one_line_code.replace(' ', comment, 1)
        return one_line_code
        
    def _get_identifier(self):
        identifier = self.rule_data.get('identifier')
        if identifier is not None:
            return identifier
        
        elif self.data_env is not None:
            try:
                config = dotenv_values()
                return config.get(self.data_env)
            except:
                raise ValueError('The parameter was not found in the configuration env')

        if self.config_file is not None and self.section is not None and self.config_key is not None :
            try:
                return self._read_config_file().get(self.section, self.config_key)
            except configparser.NoOptionError as error:
                raise ValueError('The "rule_id" parameter was not found in the configuration file.') from error

        if self.find_name is not None:
            filter_data = {
                "filter": {"and": [{"eq": {"rule.organization": self.rule_data['organization']}}]},
                "limit": {"size": 1000, "start": 1}
            }
            all_identifiers = self.with_filter(filter_data).search().build().execute().json()
            if isinstance(all_identifiers, dict) and 'rules' in all_identifiers:
                identifier_list = all_identifiers['rules']
            else:
                raise ValueError('Unexpected response format from the server.')

            name_identifier = [
                item['identifier'] for item in identifier_list if item.get('name') == self.find_name
            ]
            if name_identifier:
                return name_identifier[0]
            else:
                raise ValueError(f'No rule with the name "{self.find_name}" was found.')

        raise ValueError('A configuration file, a model identifier, or a name is required.')

    def _read_config_file(self):
        if self.config_file is not None:
            if os.path.exists(self.config_file):
                config = configparser.ConfigParser()
                config.read(self.config_file)
                return config
            raise ValueError('The configuration file does not exist.')
        return None
        
    def _execute_create(self):
        response = requests.post(self.url, headers=self.client.headers, json=self.rule_data, verify=False, timeout=3000)
        if response.status_code == 201:
            file_config = self._read_config_file()
            identifier = self._get_created_rule_identifier()
            if self.config_file:
                file_config = self._read_config_file()
                if file_config:
                    try:
                        self._read_config_file().get(self.section, self.config_key)
                        file_config.set(self.section, self.config_key, identifier)
                        with open(self.config_file, 'w', encoding='utf-8') as configfile:
                            file_config.write(configfile)
                    except configparser.NoOptionError:
                        return ValueError('The "rule_id" parameter was not found in the configuration file.')
            
                elif self.data_env is not None:
                    try:
                        env_vars = dotenv_values('.env')
                        if self.data_env not in env_vars:
                            raise KeyError('The environment variable was not found in the .env file.')
                        
                        set_key('.env', self.data_env, identifier)

                    except KeyError as error:
                        raise ValueError('The environment variable was not found in the .env file.') from error
        return response
    
    def _get_created_rule_identifier(self):
        name = self.rule_data.get('name')
        if not name:
            raise ValueError('The "name" attribute is missing or empty.')
        filter_data = {
            "filter": {"and": [{"eq": {"rule.organization": self.rule_data['organization']}}]},
            "limit": {"size": 1000, "start": 1}
        }
        all_identifiers = self.with_filter(filter_data).search().build().execute().json()
        if 'rules' in all_identifiers:
            for rule in all_identifiers['rules']:
                if 'name' in rule and rule['name'] == name:
                    return rule['identifier']

        raise ValueError(f'No rule with the name "{name}" was found.')

    def _execute_search(self) -> List[Dict[str, Any]]:
        response = requests.post(self.url, headers=self.client.headers, json=self.filter_data, verify=False, timeout=3000)
        return response
    
    def _execute_find_one(self) -> List[Dict[str, Any]]:
        response = requests.get(self.url, headers=self.client.headers, json=self.filter_data, verify=False, timeout=3000)
        return response
    
    def _execute_update(self) -> int:
        response = requests.put(self.url, headers=self.client.headers, json=self.rule_data, verify=False,timeout=3000)
        return response
        
    def _execute_delete(self) -> int:
        response = requests.delete(self.url, headers=self.client.headers, json=self.rule_data, verify=False, timeout=3000)
        return response
    
    def _execute_update_parameters(self) -> int:
        response = requests.put(self.url, headers=self.client.headers, json=self.rule_data['parameters'], verify=False, timeout=3000)
        return response
    
    def _execute_catalog(self) -> List[Dict[str, Any]]:
        response = requests.get(self.url, headers=self.client.headers, json=self.filter_data, verify=False, timeout=3000)
        return response
    
    def _execute_save(self):
        if self.data_env is not None or self.config_file is not None:
            if self.data_env is not None:
                identifier = dotenv_values('.env')[self.data_env]
                self.identifier = identifier
                
            elif self.config_file is not None:
                config = configparser.ConfigParser()
                config.read(self.config_file)
                rule_id = config.get(self.section, self.config_key, fallback=None)
                self.rule_data["identifier"] = rule_id
                response = self.find_one().build().execute().json()
                if response is not None and isinstance(response, dict):
                    #Update
                    return self.update().build().execute()
                #Create
                return self.create().build().execute()
        return ValueError('The "rule_id" parameter was not found in the configuration file.')

    def _execute_set_identifier(self):
        try:
            file_config = self._read_config_file()
            self._read_config_file().get(self.section, self.config_key)
            file_config.set(self.section, self.config_key,  self.rule_data["identifier"])
            with open(self.config_file, 'w', encoding='utf-8') as configfile:
                file_config.write(configfile)
            return ('The rule_id field in the configuration file was successfully changed.')
        
        except configparser.NoOptionError:
            return ValueError('The "rule_id" parameter was not found in the configuration file.') 
        
    def _execute_env_identifier(self) -> None:
        try:
            env_vars = dotenv_values('.env')
            if self.data_env not in env_vars:
                raise KeyError('The environment variable was not found in the .env file.')
                    
            set_key('.env', self.data_env, self.identifier)

        except KeyError as error:
            raise ValueError('The environment variable was not found in the .env file.') from error
