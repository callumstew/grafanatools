""" Generate Grafana JSON objects """
import json
from . import defaults


def fill_defaults_dashboard(dashboard,
                            default=defaults.DASHBOARD):
    out = default.copy()
    out.update(dashboard)
    return out


def fill_defaults_panel(panel, default=defaults.PANELS):
    panel_type = panel.get('type', 'graph')
    out = default[panel_type].copy()
    out.update(panel)
    return out


def fill_defaults_templating(variable,
                             default=defaults.TEMPLATING):
    templating_type = variable.get('type', 'constant')
    out = default[templating_type].copy()
    out.update(variable)
    return out


def fill_defaults_datasource(datasource,
                             default=defaults.DATASOURCES):
    datasource_type = datasource.get('type', 'graphite')
    out = default[datasource_type].copy()
    out.update(datasource)
    return out


def fill_defaults_annotation(annotation,
                             default=defaults.ANNOTATIONS):
    annotation_type = annotation.get('type', 'dashboard')
    out = default[annotation_type].copy()
    out.update(annotation)
    return out


def generate_dashboard(dashboard):
    dashboard = fill_defaults_dashboard(dashboard)
    for annotation in dashboard['annotations']:
        fill_defaults_annotation(annotation)
    for panel in dashboard['panels']:
        fill_defaults_panel(panel)
    for variable in dashboard['templating']['list']:
        fill_defaults_templating(variable)
    return dashboard


def dashboard_dumps(dashboard):
    return json.dumps(generate_dashboard(dashboard))
