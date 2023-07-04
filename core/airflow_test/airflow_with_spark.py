import json

from airflow.decorators  import dag, task
from datetime import datetime, timedelta
import pendulum

from pyspark.sql import SparkSession, DataFrame

spark = SparkSession.builder.getOrCreate()


@dag(
    'spark_tutorial',
    schedule=None,
    start_date=datetime(2022,1,1),
    tags=['spark']
)
def test_spark():
    @task()
    def load():
        sc = spark.sparkContext
        rdd = sc.parallelize(['a', 'b'])
        df = spark.createDataFrame(rdd, ['col'])
        return df
    @task(multiple_outputs=True)
    def transform(df:DataFrame):
        return df.select('col')
    @task()
    def load(df:DataFrame):
        df.write.format('text').save('/Users/guangqianglu/Documents/citi_work/bigdata_platform_implement/core/airflow_test')
        
    df = load()
    load(transform(df))
    
test_spark()