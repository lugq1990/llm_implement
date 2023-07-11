import networkx as nx
import json
import os
import pathlib

cur_path = pathlib.Path(__file__).parent.resolve()

file_name = os.path.join(cur_path, "sample_flow.json")

with open(file_name, 'r') as f:
    data = f.read()


flow_json = json.loads(data)

def load_template(file_path=None, file_name=None):
    if not file_name:
        file_name = 'sample_flow.json'
    if not file_path:
        file_name = cur_path
    file = os.path.join(file_path, file_name)
    with open(file, 'r') as f:
        data = f.read()

    flow_json = json.loads(data)
    return flow_json


# DAG should be created based on the json file
class DAG:
    # this class all related DAG
    def __init__(self) -> None:
        self._json_data = load_template()
        self.dg = nx.DiGraph()

    def create_dag(self,):
        comp_list = self._json_data['components']['1']
        node_list = [(x['id'], x) for x in comp_list]
        # first add node list
        self.dg.add_nodes_from(node_list)

        # add edge order
        for source_id, meta in node_list:
            if len(meta['connections']) > 0:
                cons = meta['connections'].get('0')
                for con in cons:
                    next_id = con['id']
                    self.dg.add_edge(source_id, next_id)
        return self.dg

    
dg = DAG().create_dag()

nx.draw_networkx(dg, with_labels=True)


from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

class Base:
    def process(self, df=None):
        raise NotImplemented("should ba called for sub-class")
    

class Source(Base):
    def process(self, df=None):
        return super().process(df)
    

class Transform(Base):
    def process(self, df=None):
        return super().process(df)
    
class Sink(Base):
    def process(self, df=None):
        return super().process(df)
    

class HiveSource(Source):
    # this could be supported for checking
    def __init__(self, **kwargs) -> None:
        database = kwargs.get('database')
        table_name =kwargs.get('tableName')
        query = kwargs.get('query')
        self.table_name = "{}.{}".format(database, table_name)
        if not query:
            query = "select * from {}".format(self.table_name)
        self.query = query
        super().__init__()
    
    def process(self, df=None):
        df = spark.sql(self.query)
        return df




def hive_source(**kwargs):
    d = kwargs.get('database')
    t = kwargs.get('tableName')
    print("get {}.{}".format(d, t))

    
def select(**kwargs):
    s = kwargs.get("selectExpression")
    print(s)
    
def hive_sink(**kwargs):
    d = kwargs.get('database')
    t = kwargs.get('tableName')
    f = kwargs.get('format')
    print('database: {}.{} with format: {}'.format(d, t, f))
    

dg = create_dag()
    
### this is core !
top_order = nx.topological_sort(dg)

for n in top_order:
    c = dg.node[n]['component']
    o = dg.node[n]['options']
    if c == 'hive_source':
        hive_source(**o)
    elif c == "select":
        select(**o)
    elif c == 'hive_sink':
        hive_sink(**o)
