import requests
import pandas as pd
from typing import Callable, Union, List, Dict, Any

class DataSetsBuilder:
    ''' Dataset Builder '''
    def __init__(self, opengate_client):
        self.client = opengate_client
        self.organization_name: str = None
        self.identifier: str = None
        self.filter_data: Dict[str, Any] = {}
        self.format_data: str = None
        self.url: str = None
        self.method: str = None
        self.requires: Dict[str, Any] = {}

    def with_organization(self, organization_name: str) -> 'DataSetsBuilder':
        ''' Sets the organization name '''
        self.organization_name = organization_name
        return self

    def with_identifier(self, identifier: str) -> 'DataSetsBuilder':
        ''' Sets the identifier '''
        self.identifier = identifier
        return self

    def with_filter(self, filter_data: Dict[str, Any]) -> 'DataSetsBuilder':
        ''' Sets the filter data '''
        self.filter_data = filter_data
        return self

    def with_format(self, format_data: str) -> 'DataSetsBuilder':
        ''' Sets the format data '''
        self.format_data = format_data
        return self

    def search(self) -> 'DataSetsBuilder':
        ''' Initiates a search '''
        self.requires = {
            'identifier': self.identifier,
            'format': self.format_data,
            'organization': self.organization_name,
        }
        self.method = 'search'
        self.url = f'{self.client.url}/north/v80/datasets/provision/organizations/{self.organization_name}/{self.identifier}/data'
        return self

    def build(self) -> 'DataSetsBuilder':
        ''' Builds the request and checks for missing parameters '''
        if self.requires is not None:
            for key, value in self.requires.items():
                assert value is not None, f'{key} is required'
        return self

    def execute(self) -> Union[int, List[Dict[str, Any]]]:
        ''' Executes the request and returns the response '''
        methods: Dict[str, Callable[[], Union[int, List[Dict[str, Any]]]]] = {
            'search': self._execute_searching
        }
        function = methods.get(self.method)
        if function is None:
            raise ValueError(f'Unsupported method: {self.method}')
        return function()

    def _execute_searching(self) -> Union[str, List[Dict[str, Any]], pd.DataFrame]:
        response = requests.post(self.url, headers=self.client.headers, json=self.filter_data, verify=False, timeout=3000)
        if response.status_code == 200:
            data = response.json()
            if self.format_data == 'csv':
                csv = ','.join(data['columns']) + '\n'
                for fila in data['data']:
                    csv += ','.join(map(str, fila)) + '\n'
                return csv
            elif self.format_data == 'dict':
                dict_data = []
                for fila in data['data']:
                    fila_dict = {data['columns'][i]: fila[i] for i in range(len(data['columns']))}
                    dict_data.append(fila_dict)
                return dict_data
            elif self.format_data == 'pandas':
                data_frame = pd.DataFrame(data['data'], columns=data['columns'])
                return data_frame
            else:
                raise ValueError('Format not valid')
        return response