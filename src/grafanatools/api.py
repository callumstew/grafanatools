""" Module for interacting with Grafana HTTP API
View https://docs.grafana.org/http_api/ for comprehensive
documentation
"""
import requests
from .generic import update

class BaseApi():
    """ Base class for Grafana HTTP API
    """

    def __init__(self, url='http://localhost:3000', session=None, **kwargs):
        self.s = requests.Session() if session is None else session
        self.url = url.rstrip('/') + '/'
        for k, v in kwargs.items():
            if isinstance(v, dict):
                update(self.s.__getattribute__(k), v)
            else:
                self.s.__setattr__(k, v)

    def request(self, method, endpoint, **kwargs):
        return self.s.request(method, self.url + endpoint, **kwargs)

    def get(self, endpoint, **kwargs):
        return self.s.get(self.url + endpoint, **kwargs)

    def head(self, endpoint, **kwargs):
        return self.s.get(self.url + endpoint, **kwargs)

    def patch(self, endpoint, **kwargs):
        return self.s.get(self.url + endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.s.get(self.url + endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.s.get(self.url + endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.s.get(self.url + endpoint, **kwargs)


