# full class that is supported for spark transformation
from abc import ABC
from pyspark.sql.functions import *
from bigdata_platform.init_config import get_spark


class Transform(ABC):
    _type = 'tranform'
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        
    def validate_params(self, **kwargs):
        pass
        
    def process(self, df):
        pass
    
    
    
class Select(Transform):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cols = kwargs.get('cols', "*")
        
    def process(self, df):
        # should be dict
        return df.select(self.cols)
    
    
class Lit(Transform):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.col_name = kwargs.get('col_name', 'new_col')
        self.col_value = kwargs.get('col_value', 'NONE') 
        
    def process(self, df):
        return df.withColumn(self.col_name, lit(self.col_value))
    
    
    
if __name__ == '__main__':
    spark = get_spark()
    df = spark.createDataFrame([(1, "John Doe", 21)], ("id", "name", "age"))

    df_select = Select(**{"cols": 'name'}).process(df)
    df_lit = Lit().process(df_select)
    df_lit.show()