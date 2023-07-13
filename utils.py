import json

def get_config():
    with open('config.json') as f:
        return json.load(f)
