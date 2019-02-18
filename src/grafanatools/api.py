""" Module for interacting with Grafana HTTP API
View https://docs.grafana.org/http_api/ for comprehensive
documentation
"""
from typing import Mapping, Optional, Any
from requests import Session, Response
from .generic import update

class BaseApi():
    """ Base class for Grafana HTTP API
    """

    def __init__(self, url: str = 'http://localhost:3000',
                 session: Session = Session(), **kwargs):
        self.s = session
        self.url = url.rstrip('/')
        for k, v in kwargs.items():
            if isinstance(v, dict):
                update(self.s.__getattribute__(k), v)
            else:
                self.s.__setattr__(k, v)

    def request(self, method: str, endpoint: str, **kwargs) -> Response:
        return self.s.request(method, self.url + endpoint, **kwargs)

    def get(self, endpoint: str, **kwargs) -> Response:
        return self.s.get(self.url + endpoint, **kwargs)

    def head(self, endpoint: str, **kwargs) -> Response:
        return self.s.head(self.url + endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> Response:
        return self.s.patch(self.url + endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Response:
        return self.s.post(self.url + endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> Response:
        return self.s.put(self.url + endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Response:
        return self.s.delete(self.url + endpoint, **kwargs)


class DashboardApi(BaseApi):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = self.url + '/api/dashboards'

    def create(self, dashboard: Mapping,
                         folder_id: int = 0,
                         overwrite: bool = False,
                         message: Optional[str] = None) -> Response:
        body = {'dashboard': dashboard,
                'folderId': folder_id,
                'overwrite': overwrite}
        if message:
            body['message'] = message
        return self.post(endpoint='/db', json=body)

    def update_dashboard(self, *args, **kwargs):
        return self.create(*args, **kwargs)

    def get_by_uid(self, uid: str) -> Response:
        return self.get(endpoint='/uid/' + uid)

    def delete_by_uid(self, uid: str) -> Response:
        return self.delete(endpoint='/uid/' + uid)

    def get_home_dashboard(self) -> Response:
        return self.get(endpoint='/home')

    def get_tags(self) -> Response:
        return self.get(endpoint='/tags')


class DatasourceApi(BaseApi):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = self.url + '/api/datasources'

    def get_all(self) -> Response:
        return self.get(endpoint='')

    def get_by_id(self, id: int) -> Response:
        return self.get(endpoint='/' + id)

    def get_by_name(self, name: str) -> Response:
        return self.get(endpoint='/name/' + name)

    def get_id_by_name(self, name: str) -> Response:
        return self.get(endpoint='/id/' + name)

    def create(self, datasource: Mapping[str, Any]) -> Response:
        return self.post(endpoint='', json=datasource)

    def update(self, id: int, datasource: Mapping[str, Any]) -> Response:
        return self.put(endpoint='/' + id, json=datasource)

    def delete_by_id(self, id: int) -> Response:
        return self.delete(endpoint='/' + id)

    def delete_by_name(self, name: str) -> Response:
        return self.delete(endpoint='/name/' + name)


class FoldersApi(BaseApi):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = self.url + '/api/folders'

    def get_all(self, limit: Optional[int] = None) -> Response:
        return self.get('', params={'limit': limit} if limit else None)

    def get_by_uid(self, uid: str) -> Response:
        return self.get('/' + uid)

    def get_by_id(self, id: int) -> Response:
        return self.get('/id/' + id)

    def create(self, title: str, uid: Optional[str] = None) -> Response:
        folder = {'title': title}
        if uid:
            folder['uid'] = uid
        return self.post('', json=folder)

    def update(self, uid: str, folder: Mapping[str, Any]) -> Response:
        return self.put('/' + uid, json=folder)

    def delete(self, uid: str) -> Response:
        return self.delete('/' + uid)


class GrafanaApi(BaseApi):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dashboards = DashboardApi(self.url, self.s)
        self.datasources = DatasourceApi(self.url, self.s)
        self.folders = FoldersApi(self.url, self.s)

    def search(self, **params) -> Response:
        """ Search Grafana dashboards and folders.
        Not specifying a query should return all dashboards and folders.
        Args:
            query (str): Search query (optional)
            type (str): 'dash-folder' or 'dash-db' (optional)
            tag (List[str]): List of tags (optional)
            dashboardIds (List[str]): List of dashboard id's to search (optional)
            folderIds (List[str]): List of folder id's to search (optional)
            starred (bool): Whether to search only starred items
            limit (int): Limit of results to return
        Returns:
            requests.Response
        """
        return self.get('/api/search', params=params)

    def get_all_dashboards(self):
        dashboards = self.search(type='dash-db')
        return [self.dashboards.get(db['uid']) for db in dashboards]
