""" Generate Grafana JSON objects """
import json
from copy import deepcopy
from . import defaults


def fill_template_dashboard(dashboard,
                            template=defaults.DASHBOARD):
    out = deepcopy(template)
    out.update(dashboard)
    return out


def fill_template_panel(panel, template=defaults.PANELS):
    panel_type = panel.get('type', 'graph')
    out = deepcopy(template.get(panel_type, {}))
    out.update(panel)
    return out


def fill_template_templating(variable,
                             template=defaults.TEMPLATING):
    templating_type = variable.get('type', 'constant')
    out = deepcopy(template.get(templating_type, {}))
    out.update(variable)
    return out


def fill_template_datasource(datasource,
                             template=defaults.DATASOURCES):
    datasource_type = datasource.get('type', 'graphite')
    out = deepcopy(template.get(datasource_type, {}))
    out.update(datasource)
    return out


def fill_template_annotation(annotation,
                             template=defaults.ANNOTATIONS):
    annotation_type = annotation.get('type', 'dashboard')
    out = deepcopy(template.get(annotation_type, {}))
    out.update(annotation)
    return out


def generate_dashboard(db):
    db = fill_template_dashboard(db)
    db['panels'] = [fill_template_panel(p)
                    for p in db['panels']]
    db['templating']['list'] = [fill_template_templating(v)
                                for v in db['templating']['list']]
    db['annotations']['list'] = [fill_template_annotation(a)
                                 for a in db['annotations']['list']]
    return db


def dashboard_dumps(dashboard):
    return json.dumps(generate_dashboard(dashboard))
