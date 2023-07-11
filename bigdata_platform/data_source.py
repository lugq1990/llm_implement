from bigdata_platform.init_config import get_spark
import os

spark = get_spark()


class DataSource:
    _type = 'source'
    def __init__(self, *args, **kwargs) -> None:
        pass

    def validate(self):
        pass
    
    def process(self):
        pass


class JDBCSource(DataSource):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.url = kwargs.get('url', 'localhost:3306')
        self.database = kwargs.get('database', 'spark')
        self.table_name = kwargs.get('tableName', 'source')
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
    
    
class FileSource(DataSource):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # todo: change this path
        file_path = kwargs.get('file_path', r'D:\work\code_related\my_codes\llm_implement')
        file_name = kwargs.get('file_name', 'test.txt')
        self.file_type = kwargs.get('file_type', 'txt')
        self.file_path = os.path.join(file_path, file_name)
    
    def process(self):
        if self.file_type == 'json':
            df = spark.read.option("multiline","true").format(self.file_type).load(self.file_path)    
        elif self.file_type == 'txt':
            df = spark.read.text(self.file_path)
        return df
    

if __name__ == '__main__':    
    df = FileSource().process()