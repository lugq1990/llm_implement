import networkx as nx
import json
import os
import pathlib
import sys
# add this to avoid import error.
sys.path.append(r'D:\work\code_related\my_codes\llm_implement')

from bigdata_platform.func_mapping import *


def load_template(file_path=None, file_name=None):
    if not file_name:
        file_name = 'sample_flow.json'
    if not file_path:
        file_path = str(pathlib.Path(__file__).parent.resolve())
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



def process_pipeline(top_order):
    data_mapping = {}

    for i, id in enumerate(top_order):
        node_params =  dg.nodes[id]
        component = node_params.get('component')
        options = node_params.get('options')
        func_class = func_mapping.get(component)(**options)
        print(component, func_class)
        if isinstance(func_class, DataSource):
            # only source type that don't need source df
            df = func_class.process()
        else:
            pre_df = data_mapping.get(top_order[i-1])
            df = func_class.process(pre_df)
        data_mapping[id] = df
        print(data_mapping)
    return data_mapping

    
if __name__ == '__main__':
    dg = DAG().create_dag()
    top_order = list(nx.topological_sort(dg))
    process_pipeline(top_order=top_order)