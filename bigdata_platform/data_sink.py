from bigdata_platform.init_config import get_spark
import os

spark = get_spark()


class DataSink:
    _type = 'sink'
    def __init__(self, *args, **kwargs) -> None:
        pass

    def validate(self):
        pass
    
    def process(self):
        pass


class JDBCSource(DataSink):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.url = kwargs.get('url', 'localhost:3306')
        self.database = kwargs.get('database', 'spark')
        self.table_name = kwargs.get('table_name', 'source')
        self.jdbc = 'jdbc:mysql://{}/{}'.format(self.url, self.database)
        self.mysql_properties = {
            "user": "root",
            "password": "1234",
            "driver": "com.mysql.jdbc.Driver"
        }
            
    def process(self):
        df = spark.read.format("jdbc") \
            .option("url", self.url) \
            .option("dbtable", self.table_name) \
            .option("user", self.mysql_properties["user"]) \
            .option("password", self.mysql_properties["password"]) \
            .option("driver", self.mysql_properties["driver"]) \
            .load()

        return df
    
    
class FileSink(DataSink):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # todo: change this path
        file_path = kwargs.get('file_path', r'D:\work\code_related\my_codes\llm_implement')
        file_name = kwargs.get('file_name', 'test')
        self.file_type = kwargs.get('file_type', 'csv')
        self.save_mode = kwargs.get('save_mode', 'overwrite')
        self.file_path = os.path.join(file_path, file_name)
    
    def process(self, df):
        if self.file_type == 'json':
            df.write.mode(self.save_mode).option("multiline","true").format(self.file_type).save(self.file_path)    
        elif self.file_type == 'csv':
            df.write.mode(self.save_mode).format(self.file_type).save(self.file_path)
    

if __name__ == '__main__':
    df = spark.createDataFrame([(1, "John Doe", 21)], ("id", "name", "age"))
    FileSink().process(df)