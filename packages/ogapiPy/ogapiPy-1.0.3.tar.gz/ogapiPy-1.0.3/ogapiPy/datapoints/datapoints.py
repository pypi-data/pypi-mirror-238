# pylint: disable=E0401
# pylint: disable=W0611
# pylint: disable=C0303
# pylint: disable=W0105
# pylint: disable=C0301

import requests
import json
import pandas as pd
from jsonpath_ng import parse
from io import StringIO
import numpy as np
import urllib3
from typing import Callable, Union, List, Dict, Any

class DataPointsBuilder:
    ''' Builder datapoints '''
    def __init__(self, opengate_client):
        self.client = opengate_client
        self.filter_data: Dict[str, Any] = {}
        self.transpose: bool = False
        self.mapping: Union[None, Dict[str, Dict[str, str]]] = None
        self.is_built: bool = False
        self.url: Union[None, str] = None
        self.method: Union[None, str] = None
        self.requires: Dict[str, Any] = {}

    def with_filter(self, filter_data: Dict[str, Any]) -> 'DataPointsBuilder':
        ''' filter '''
        self.filter_data = filter_data
        return self

    def with_transpose(self) -> 'DataPointsBuilder':
        ''' transpose '''
        if self.mapping is not None:
            raise ValueError('Cannot use with_transpose and with_mapped_transpose together')
        self.transpose = True
        return self

    def with_mapped_transpose(self, mapping: Dict[str, Dict[str, str]]) -> 'DataPointsBuilder':
        ''' mapped '''
        if self.transpose:
            raise ValueError('Cannot use with_mapped_transpose and with_transpose together')
        self.mapping = mapping
        return self

    def search(self) -> 'DataPointsBuilder':
        ''' search'''
        if self.mapping is not None:
            self.requires = {
                'mapping': self.mapping
        }
        elif self.transpose:
            self.requires = {
                'transpose': self.transpose
        }
        self.client.headers.update({
            'Content-type': 'application/json',
            'Accept': 'text/plain',
        })
        self.method = 'search'
        self.url = f'{self.client.url}/north/v80/search/datapoints'
        return self
   
    def build(self) -> 'DataPointsBuilder':
        ''' Builder and check if any parameter is missing. '''
        self.is_built = True
        if self.requires is not None:
            for key, value in self.requires.items():
                assert value is not None, f'{key} is required'
        return self

    def execute(self) -> Union[int, List[Dict[str, Any]], pd.DataFrame]:
        ''' Execute search '''
        methods: Dict[str, Callable[[], Union[int, List[Dict[str, Any]]]]] = {
            'search': self._execute_searching
        }
        function = methods.get(self.method)
        if function is None:
            raise ValueError(f'Unsupported method: {self.method}')
        return function()

    def _transpose_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data = data.pivot_table(index=['at', 'entity'], columns='datastream', fill_value=np.nan, aggfunc='first')
        data = data.sort_values(by='at')
        data = data['value']
        data = data.reset_index()
        return data
    
    def _execute_searching(self) -> Union[str, List[Dict[str, Any]], pd.DataFrame]:
        response = requests.post(self.url, headers=self.client.headers, json=self.filter_data, verify=False, timeout=3000)
        if response.status_code == 200:
            data_str = StringIO(response.content.decode('utf-8'))
            data = pd.read_csv(data_str, sep=';')

            if self.transpose:
                data = self._transpose_data(data)
            if self.mapping:
                data = self._transpose_data(data)
                for column, sub_complexdata in self.mapping.items():
                    if column in data.columns:
                        json_path_expressions = {key: parse(value) for key, value in sub_complexdata.items()}

                        for row_index, cell_value in data[column].items():
                            if not pd.isna(cell_value):
                                for key, json_path_expr in json_path_expressions.items():
                                    matches = json_path_expr.find(json.loads(cell_value))
                                    if matches:
                                        new_column = f'{key}'
                                        if new_column not in data.columns:
                                            data[new_column] = None
                                        data.at[row_index, new_column] = matches[0].value
                                        

            return data
        return response

