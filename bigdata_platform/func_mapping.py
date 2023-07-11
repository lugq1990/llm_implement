# func mapping utils that could be used to init transformation


from tranforms import *
from data_sink import *
from data_source import *

func_mapping = {
    'hive_source':'',
    'select': Select,
    'lit': Lit,
    'file_source': FileSource,
    'file_sink': FileSink
}