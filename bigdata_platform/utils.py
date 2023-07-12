import os
import json
import pathlib


def load_template(file_path=None, file_name=None) -> json:
    if not file_name:
        file_name = 'sample_flow.json'
    if not file_path:
        file_path = str(pathlib.Path(__file__).parent.resolve())
    file = os.path.join(file_path, file_name)
    with open(file, 'r') as f:
        data = f.read()

    flow_json = json.loads(data)
    flow_json = _convert_bool_str_to_boolean(flow_json)
    return flow_json


def _convert_bool_str_to_boolean(config):
    # convert airflow config that is string boolean types to Boolean
    airflow_default_keys = config['airflow_config']['default_args']
    for k, v in airflow_default_keys.items():
        if isinstance(v, str) and v.lower() in ['true', 'false']:
            if v.lower() == 'true':
                v = True
            elif v.lower() == 'false':
                v = False
            else:
                print("Not supported types")
            airflow_default_keys[k] = v
    config['airflow_config']['default_args'] = airflow_default_keys
    return config


print(load_template().keys())