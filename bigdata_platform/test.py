from pyspark.sql import SparkSession


if __name__ == "__main__":
    spark = SparkSession.builder.getOrCreate()
    df = spark.createDataFrame([(1, "John Doe", 21)], ("id", "name", "age"))

    df.show()