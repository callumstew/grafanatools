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
    out = deepcopy(template[panel_type])
    out.update(panel)
    return out


def fill_template_templating(variable,
                             template=defaults.TEMPLATING):
    templating_type = variable.get('type', 'constant')
    out = deepcopy(template[templating_type])
    out.update(variable)
    return out


def fill_template_datasource(datasource,
                             template=defaults.DATASOURCES):
    datasource_type = datasource.get('type', 'graphite')
    out = deepcopy(template[datasource_type])
    out.update(datasource)
    return out


def fill_template_annotation(annotation,
                             template=defaults.ANNOTATIONS):
    annotation_type = annotation.get('type', 'dashboard')
    out = deepcopy(template[annotation_type])
    out.update(annotation)
    return out


def generate_dashboard(dashboard):
    dashboard = fill_template_dashboard(dashboard)
    for annotation in dashboard['annotations']:
        fill_template_annotation(annotation)
    for panel in dashboard['panels']:
        fill_template_panel(panel)
    for variable in dashboard['templating']['list']:
        fill_template_templating(variable)
    return dashboard


def dashboard_dumps(dashboard):
    return json.dumps(generate_dashboard(dashboard))
