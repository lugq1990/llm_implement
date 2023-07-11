import os
import json
import peft


def load_keys():
    with open('openai.keys', 'r') as f:
        data = f.read()
    
    return json.loads(data)


if __name__ == '__main__':
    print(load_keys())