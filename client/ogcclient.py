import requests

from client import cmdmapping
from client import constant
from client.constant import JSON_TYPE
from client.utils import merge_dictionaries


class OgcApiClient:

    def __init__(
            self,
            host: str,
            accept_type: str = JSON_TYPE,
            http_headers=None
    ) -> None:
        # set host
        self.host = host
        # set http header
        headers = {}
        if http_headers is None:
            http_headers = {}
        if accept_type == constant.JSON_TYPE:
            headers['accept'] = 'application/json'
        elif accept_type == constant.HTML_TYPE:
            headers['accept'] = 'html/text'
        self.headers = merge_dictionaries(headers, http_headers)

    def map_url(self, key: str, path_format=None) -> str:
        if path_format is None:
            path_format = {}
        return self.host + cmdmapping.URL_MAP.get(key).format(**path_format)

    def desc(self):
        http_resp = requests.get(self.map_url(cmdmapping.DESC), headers=self.headers)
        return http_resp.text

    def conformance(self):
        http_resp = requests.get(self.map_url(cmdmapping.CONFORMANCE), headers=self.headers)
        return http_resp.text

    def list_collections(self):
        http_resp = requests.get(self.map_url(cmdmapping.LIST_COLLECTIONS), headers=self.headers)
        return http_resp.text

    def get_collection_by_id(self, collection_id: str):
        http_resp = requests.get(
            self.map_url(cmdmapping.GET_COLLECTION_BY_ID_KEY, {'collectionId': collection_id}),
            headers=self.headers
        )
        return http_resp.text

    def list_collection_items_by_id(self, collection_id: str) -> str:
        http_resp = requests.get(
            self.map_url(cmdmapping.LIST_COLLECTION_ITEMS_BY_ID_KEY, {'collectionId': collection_id}),
            headers=self.headers
        )
        return http_resp.text
