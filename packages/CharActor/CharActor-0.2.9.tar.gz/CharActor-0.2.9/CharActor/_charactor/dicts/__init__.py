import os
import json

def load_json(path):
    """Load a JSON file from the given path."""
    with open(path, 'r') as f:
        return json.load(f)
    
# Desc: Loads dicts from JSON files
_dicts = [d[:-5] for d in os.listdir(os.path.abspath(os.path.dirname(__file__))) if d.endswith('.json') and d != '__init__.py']


def load_dict(name):
    if name in _dicts:
        return load_json(f'{os.path.join(os.path.dirname(__file__), name)}.json')
    else:
        raise ValueError(f'No such dict: {name}')
    
def load_all_dicts():
    return {d: load_dict(d) for d in _dicts}

# Desc: Loads lists from text files
_lists = [d[:-9] for d in os.listdir(os.path.dirname(__file__)) if d.endswith('_list.txt') and d != '__init__.py']

def load_list(name):
    if name not in _lists:
        raise ValueError(f'No such list: {name}')
    with open(f'{os.path.join(os.path.dirname(__file__), name)}_list.txt', 'r') as f:
        return [l.strip() for l in f.readlines()]