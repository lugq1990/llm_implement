from datetime import datetime, timedelta
from airflow import DAG

from airflow.operators.bash import BashOperator

with DAG(
    "base_flow",
    schedule=timedelta(days=1),
    start_date=datetime(2021,1,1),
    tags=['exampel;']
) as dag:
    t1 = BashOperator(task_id='print_da', bash_command='date')
    t2 = BashOperator(task_id='sleep', bash_command='sleep 1', retries=3)
    
    t1 >> t2