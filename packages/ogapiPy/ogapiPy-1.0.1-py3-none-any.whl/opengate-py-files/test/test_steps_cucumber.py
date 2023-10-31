''' Steps for the features '''
import sys
import os
import configparser
import pytest
from pytest_bdd import scenarios, given, when, then, parsers, step
from behave import step
import ast
import time
import re
import pandas as pd
from io import StringIO
import json
import re
from test.ownworld import testing_data


#Scenarios feature execute config file pytest.ini 'bdd_features_base_dir'

scenarios('ia/model.feature')
scenarios('ia/transformers.feature')
scenarios('ia/pipelines.feature')
scenarios('rules/rules.feature')
scenarios('entities/entities.feature')
scenarios('datasets/datasets.feature')
scenarios('timeseries/timeseries.feature')
scenarios('datapoints/datapoints.feature')

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(current_dir, '..')
sys.path.append(project_dir)

from ai_models.ai_models import AIModelsBuilder
from ai_transformers.ai_transformers import AITransformersBuilder
from ai_pipelines.ai_pipelines import AIPipelinesBuilder
from rules.rules import RulesBuilder
from entities.entities import EntitiesBuilder
from datasets.datasets import DataSetsBuilder
from timeseries.timeseries import TimeSeriesBuilder
from datapoints.datapoints import DataPointsBuilder

#Cambiar esto por el nombre final
from opengate_client import OpenGateClient

config = configparser.ConfigParser()
config_file_path = os.path.join(current_dir, 'config_test.ini')
config.read(config_file_path)

ai_builder_instance = None

@pytest.fixture
def client():
    ''' client '''
    api_url = config.get('opengate', 'url')
    api_user = config.get('opengate', 'user')
    api_password = config.get('opengate', 'password')
    return OpenGateClient(url=api_url, user=api_user, password=api_password)

@pytest.fixture
@given(parsers.parse('I want to build a "{build_type}"'))
def ai_builder(client, build_type):
    ''' Choose AI model or transformer '''
    global ai_builder_instance
    if build_type == 'model':
        ai_builder_instance = AIModelsBuilder(client)
    elif build_type == 'transformer':
        ai_builder_instance = AITransformersBuilder(client)
    elif build_type == 'pipeline':
        ai_builder_instance = AIPipelinesBuilder(client)
    elif build_type == 'rule':
        ai_builder_instance = RulesBuilder(client)
    elif build_type == 'entity':
        ai_builder_instance = EntitiesBuilder(client)
    elif build_type == 'dataset':
        ai_builder_instance = DataSetsBuilder(client)
    elif build_type == 'timeserie':
        ai_builder_instance = TimeSeriesBuilder(client)
    elif build_type == 'datapoint':
        ai_builder_instance = DataPointsBuilder(client)
    else:
        raise ValueError(f'Invalid builder type: {build_type}')
    return ai_builder_instance

@given(parsers.parse('I want to use organization "{organization}"'))
def step_organization(organization):
    ''' organization '''
    ai_builder_instance.with_organization(get_value_from_path(testing_data, organization))

@given(parsers.parse('I want to use an artificial intelligence file "{file}"'))
def step_file(file):
    ''' file tod add '''
    ai_builder_instance.add_file(file)

@given(parsers.parse('I want to save id in a configuration file "{config_file}"'))
def step_set_id_config_file(config_file):
    ''' config file to use '''
    ai_builder_instance.with_config_file(config_file)

@given(parsers.parse('I want to search id in a configuration file "{config_file}"'))
def step_search_id_config_file(config_file):
    ''' search id in confid file '''
    ai_builder_instance.with_config_file(config_file, 'id', 'model_id')

@given(parsers.parse('I want to search by name "{name}"'))
def step_search_by_name(name):
    ''' search by name '''
    ai_builder_instance.with_find_by_name(name)

@given(parsers.parse('I want to download with name "{name}"'))
def step_save_outuput_file(name):
    ''' Save outuput file '''
    ai_builder_instance.with_output_file_path(name)

@when(parsers.parse('I want to remove with name "{name}"'))
def step_remove_outuput_file(name):
    ''' Remove outuput file '''
    current_file = os.path.abspath(name)
    os.remove(current_file)

@given(parsers.parse('I want to use a prediction "{prediction}"'))
def step_prediction_code(prediction):
    ''' Prediction '''
    predic = ast.literal_eval(prediction)
    ai_builder_instance.with_prediction(predic)

@given(parsers.parse('I want to use a evaluate transformer "{prediction}"'))
def step_evaluate_code(prediction):
    ''' Evaluate '''
    predic = ast.literal_eval(prediction)
    ai_builder_instance.with_evaluate(predic)

@given(parsers.parse('I want to use a file name download transform "{file_name}"'))
def step_file_name(file_name):
    ''' file name download transform '''
    ai_builder_instance.with_file_name(file_name)

@given(parsers.parse('Set identifier in configuration file with section "{section}" and key {key} and {value} with identifier "{identifier}"'))
def step_identifier_config(section, key, identifier):
    ''' Step set identifier '''
    config.set(section, key, identifier)

@given(parsers.parse('I want to use a identifier "{identifier}"'))
def step_identifier(identifier):
    ''' identifier '''
    ai_builder_instance.with_identifier(get_value_from_path(testing_data, identifier))

@given(parsers.parse('I want add action "{add_action}"'))
def step_add_action(add_action):
    ''' file add action '''
    ai_builder_instance.add_action(add_action)

@given(parsers.parse('I want to use a name "{name}"'))
def step_with_name(name):
    ''' with name '''
    ai_builder_instance.with_name(name)

@given(parsers.parse('I want to use a filter "{filter_data}"'))
def step_with_filter(filter_data):
    ''' filter '''
    ai_builder_instance.with_filter(ast.literal_eval(filter_data))

@given(parsers.parse('I want to use a channel "{channel}"'))
def step_with_channel(channel):
    ''' channel '''
    ai_builder_instance.with_channel(get_value_from_path(testing_data, channel))

@given(parsers.parse('I want to use a active "{active_rule}"'))
def step_with_rule(active_rule):
    ''' active rule '''
    ai_builder_instance.with_active(get_value_from_path(testing_data, active_rule))

@given(parsers.parse('I want to use a mode "{mode}"'))
def step_with_mode(mode):
    ''' mode '''
    ai_builder_instance.with_mode(get_value_from_path(testing_data, mode))

@given(parsers.parse('I want to use a type "{type_data}"'))
def step_with_type(type_data):
    ''' type '''
    ai_builder_instance.with_type(ast.literal_eval(type_data))

@given(parsers.parse('I want to use a condition "{condition}"'))
def step_with_condition(condition):
    ''' actions delay '''
    ai_builder_instance.with_condition(ast.literal_eval(condition))

@given(parsers.parse('I want to use a actions delay "{actions_delay}"'))
def step_with_actions_delay(actions_delay):
    ''' actions delay '''
    ai_builder_instance.with_actions_delay(get_value_from_path(testing_data, actions_delay))

@given(parsers.parse('I want to use a actions "{actions}"'))
def step_with_actions(actions):
    ''' actions '''
    ai_builder_instance.with_actions(ast.literal_eval(actions))

@given(parsers.parse('I want to use a code "{code}"'))
def step_with_code(code):
    ''' code '''
    ai_builder_instance.with_code(code)

@given(parsers.parse('I want to use a parameters "{parameters}"'))
def step_with_parameters(parameters):
    ''' parameters '''
    ai_builder_instance.with_parameters(ast.literal_eval(parameters))

@given(parsers.parse('I want to use a format "{format_path}"'))
def step_with_format(format_path):
    ''' format '''
    ai_builder_instance.with_format(get_value_from_path(testing_data, format_path))

@given(parsers.parse('I want to use a transpose'))
def step_with_transpose():
    ''' transpose '''
    ai_builder_instance.with_transpose()

@given(parsers.parse('I want to use a mapping "{mapping_transpose}"'))
def step_with_mapped_transpose(mapping_transpose):
    ''' mapping '''
    ai_builder_instance.with_mapped_transpose(ast.literal_eval(mapping_transpose))

@then(parsers.parse('I wait "{number_second}" seconds'))
def step_wait_seconds(number_second):
    ''' timeSleep '''
    time.sleep(number_second)

@when('I create')
def step_create():
    ''' Step create'''
    ai_builder_instance.create()

@when('I update')
def step_update():
    ''' Step update '''
    ai_builder_instance.update()

@when('I find all')
def step_find_all():
    ''' Step find all '''
    ai_builder_instance.find_all()

@when('I find one')
def step_find_one():
    ''' Step find one '''
    ai_builder_instance.find_one()

@when('I validate')
def step_validate():
    ''' Step find one '''
    ai_builder_instance.validate()

@when('I download')
def step_download():
    ''' Step download '''
    ai_builder_instance.download().build().execute()

@when('I prediction')
def step_prediction():
    ''' Step download '''
    ai_builder_instance.prediction()

@when('I evaluate transformer')
def step_evaluate():
    ''' Step download '''
    ai_builder_instance.evaluate()

@when('I save')
def step_save():
    ''' Step save '''
    ai_builder_instance.save()

@when('I delete')
def step_delete():
    ''' Step delete '''
    ai_builder_instance.delete()

@when('I search')
def step_search():
    ''' Step search '''
    ai_builder_instance.search()

@when('I catalog')
def step_catalog():
    ''' Step catalog '''
    ai_builder_instance.catalog()

@when('I update parameters')
def step_update_parameters():
    ''' Step parameters '''
    ai_builder_instance.update_parameters()

@then(parsers.parse('The response should be "{status_code}"'))
def step_status_code(status_code):
    '''Step_then_the_response_should_be'''
    response = ai_builder_instance.build().execute()
    assert response.status_code == int(status_code)

@then(parsers.parse('The prediction should be "{prediction}"'))
def step_prediction_result(prediction):
    ''' Step The prediction should be'''
    response = ai_builder_instance.build().execute()
    predic = ast.literal_eval(prediction)
    ai_builder_instance.with_prediction(predic)
    assert response.json() == predic
    time.sleep(2)

@then(parsers.parse('The identifier in config field should be "{identifier}"'))
def step_set_identifier(identifier):
    '''Step_then identifier in config field should be'''
    ai_builder_instance.set_config_file_identifier().build().execute()
    get_identifier = config.get('id', 'model_id')
    assert get_identifier == identifier

@then(parsers.parse('The response search should be "{expected_type}"'))
def step_response_should_be_expected_type_search(expected_type):
    ''' expected type search '''
    response_data = ai_builder_instance.build().execute()
    if expected_type == 'dict':
        assert isinstance(response_data, list), 'is not a dict'
    elif expected_type == 'csv':
        assert isinstance(response_data, str), 'is not a csv'
    elif expected_type == 'pandas':
        assert isinstance(response_data, pd.DataFrame), 'is not a pandas DataFrame'
    else:
        raise ValueError(f'Unsupported data type for test: {expected_type}')

@then(parsers.parse('verify table values:\n{attr_value_table}'))
def verify_table_values(attr_value_table):
    ''' compare table '''
    pd_datapoints = ai_builder_instance.build().execute()
    
    attr_value_df = pd.read_csv(StringIO(attr_value_table), sep='|', skipinitialspace=True)
    
    attr_value_df.columns = attr_value_df.columns.str.strip()
    columns_to_drop = [col for col in attr_value_df.columns if col.startswith('Unnamed')]
    attr_value_df.drop(columns=columns_to_drop, inplace=True)
    attr_value_df.replace("NaN", None, inplace=True, regex=True)
    attr_value_df.replace("None", None, inplace=True, regex=True)
    
    pd_datapoints_json = pd_datapoints.to_json(orient='records', date_format='iso', date_unit='s')
    attr_value_json = attr_value_df.to_json(orient='records', indent=4)
    
    pd_datapoints_records = json.loads(pd_datapoints_json)
    attr_value_records = json.loads(attr_value_json)
    
    for record in attr_value_records:
        for key in record:
            if isinstance(record[key], str):
                record[key] = re.sub(r'\s+', ' ', record[key]).strip()

    assert pd_datapoints_records == attr_value_records, "Data does not match"

def get_value_from_path(data_dict, path):
    ''' search path in objet ownword.py'''
    keys = path.split('.')
    value = data_dict
    for key in keys:
        value = value.get(key)
        if value is None:
            raise ValueError(f'Invalid path: {path}')
    return value
