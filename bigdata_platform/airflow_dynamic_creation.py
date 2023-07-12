from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import dag, task
from airflow.operators.bash_operator import BashOperator
import sys
# add this to avoid import error.
sys.path.append(r'D:\work\code_related\my_codes\llm_implement')
from bigdata_platform.utils import load_template


# config_path = str(Path(__file__).parent.resolve())

# def load_yaml_file(file_name):
#     file_path = os.path.join(config_path, file_name)
#     with open(file_path, 'r') as f:
#         config = yaml.safe_load(f)
#     config = _convert_schedule_list_to_string(config)
#     config = _convert_string_date_to_datetime(config)
#     return config


def _convert_string_date_to_datetime(config):
    start_date = config['default_args'].get('start_date')
    start_date = datetime.strptime(start_date, '%Y%m%d')
    config['default_args']['start_date'] = start_date
    return config
    

def _convert_schedule_list_to_string(config):
    schedule_type = config['default_args'].get('schedule')
    print(schedule_type)
    if schedule_type == 'hour':
        schedule_type = "@hourly"
    elif schedule_type == 'daily':
        schedule_type = "@daily"
    elif schedule_type == 'hour':
        schedule_type = "@weekly"
    elif schedule_type == 'weekly':
        schedule_type = "@hourly"
    elif schedule_type == 'monthly':
        schedule_type = "@monthly"
    elif schedule_type == 'yearly':
        schedule_type = "@yearly"
    elif schedule_type == 'once':
        schedule_type = "@once"
    else:
        raise ValueError("Couldn't get schedule type supported")
    config['default_args']['schedule'] = schedule_type
    return config
    


def build_spark_submit_command(params):
    cmd = ["spark-submit --deploy-mode client"]
    if 'conf' in params:
        for key in params['conf']:
            cmd += ["--conf", "{}={}".format(key, str(params['conf'][key]))]
    if 'queue' in params:
        cmd += ["--queue", params['queue']]
    if 'jars' in params:
        cmd += ["--jars", params['jars']]
    if 'num_executors' in params:
        cmd += ["--num-executors", str(params['num_executors'])]
    if 'total_executor_cores' in params:
        cmd += ["--total-executor-cores", str(params['total_executor_cores'])]
    if 'executor_cores' in params:
        cmd += ["--executor-cores", str(params['executor_cores'])]
    if 'executor_memory' in params:
        cmd += ["--executor-memory", params['executor_memory']]
    if 'driver_memory' in params:
        cmd += ["--driver-memory", params['driver_memory']]
    if 'name' in params:
        cmd += ["--name", params['name']]
    if 'java_class' in params:
        cmd += ["--class", params['java_class']]
    if 'verbose' in params:
        cmd += ["--verbose"]
    if 'application' in params:
        cmd += [params['application']]
    if 'application_args' in params:
        cmd += params['application_args']

    print("Spark-Submit cmd: %s" % ' '.join(cmd))
    return ' '.join(cmd)


if __name__ == "__main__":
    # this config will be auto generated.
    config = load_template()
    airflow_config = config['airflow_config']
    airflow_config = _convert_schedule_list_to_string(airflow_config)
    airflow_config = _convert_string_date_to_datetime(airflow_config)
    print(airflow_config)
    dag = DAG(airflow_config.get('dag_id'), default_args=airflow_config.get('default_args'))

    spark_submit_task = BashOperator(
        task_id=config.get("task_id"),
        bash_command=build_spark_submit_command(dict(
            name="spark",
            driver_memory='4g',
            num_executors=1,
            executor_cores=1,
            executor_memory='4g',
            queue="queue"
        )),
        dag=dag
    )
    
    dag.test()