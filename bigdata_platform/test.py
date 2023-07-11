import json
import pathlib
import os

file = os.path.join(pathlib.Path(__file__).parent.resolve(), 'sample_flow.json')

with open(file, 'r') as f:
    data = f.read()
    
print(json.loads(data))