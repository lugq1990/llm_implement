import findspark
from pyspark.sql import SparkSession

# ensure that we could get spark config
findspark.init()

spark = None


def get_spark(app_name=None):
    # .config('spark.jars', r'C:\Users\MLoong\Downloads\mysql-connector-java-8.0.27.jar') \
    global spark    
    if not app_name:
        app_name = 'bigdata_platform'
    if spark is None:
        spark = SparkSession.builder.appName(app_name).getOrCreate()
    return spark
    
    
if __name__ == '__main__':
    spark = get_spark()
    