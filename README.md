# Grafana Tools

A python tool to programmatically create grafana dashboards and upload 
them using the HTTP API.

Another similar tool, [grafanalib](https://github.com/weaveworks/grafanalib), already exists,
and is more fully featured, but seems to require writing out dashboards using the library's 
classes. This package has optional support for some Grafana objects in a similar syntax to grafanalib, but is designed to work seemlessly with the normal Grafana JSON representation. This can be useful where dashboards already exist within Grafana that you do not want to rewrite in a python-class-specific template. 

## grafanatools.api

The api module provides a thin wrapper around the
[Grafana HTTP API](http://docs.grafana.org/http_api/).

Currently only the Dashboard, Datasource Folders, and Search APIs are present,
although other endpoints can be specified manually. Both user/pass and token 
authorization are supported.

```python3
from grafanatools.api import GrafanaApi
gf = GrafanaApi(auth=('admin', 'password'))
db = gf.dashboards.get_by_uid('dashboard_uid')
db['title'] = 'Updated title'
gf.dashboards.update_dashboard(db)
```


## grafanatools.items

All Grafana objects (including dashboards as in the example above) are simply the python representation of the normal Grafana JSON object. This module contains classes that can be used instead of a dictionary (or whatever other normal JSON object is used). Currently it only contains classes for Variable objects.

e.g.
```
from grafanatools.items import Constant
db['templating'].append(Constant(name='Const', value='5'))
```

## grafanatools.generate
Rather than having to write the entire JSON object, this module will fill default values.
The `generate_dashboard` function will take a dashboard dict object and fill
the default values, given in the json files in the defaults folder, for the dashboard
and each nested panel / variable / etc.

```
from grafanatools.generate import generate_dashboard
db = {
    'title': 'Dashboard',
    'panels': [{
        'title': 'Graph plot',
        'type': 'graph'
    }]
}
db = generate_dashboard(db)
```
