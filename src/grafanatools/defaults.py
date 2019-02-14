""" Python objects of blank Grafana objects """
import os
import json

_ROOT = os.path.abspath(os.path.dirname(__file__))
_JSON_PATH = os.path.join(_ROOT, 'defaults')


def load_folder(path):
    """ Load default objects from JSON files """
    out = {}
    for fn in os.listdir(os.path.join(_JSON_PATH, path)):
        with open(os.path.join(_JSON_PATH, path, fn), 'r') as f:
            out[fn.split('.')[0]] = json.load(f)
    return out


with open(os.path.join(_JSON_PATH, 'dashboard.json')) as dbf:
    DASHBOARD = json.load(dbf)

PANELS = load_folder('panels')
TEMPLATING = load_folder('templating')
DATASOURCES = load_folder('datasources')
ANNOTATIONS = load_folder('annotations')
