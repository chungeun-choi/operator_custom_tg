from airflow.hooks.base import BaseHook
from requests.sessions import Session



class MovielensHook(BaseHook):
    DEFAULT_HOST = "movielens"
    DEFAULT_SCHEMA = "http"
    DEFAULT_PORT = 5000

    def __init__(self, conn_id,context=None):
        super().__init__(context)
        self._conn_id = conn_id
        self._session = None
        self._base_url = None

    def get_conn(self) -> Session:

        if self._session is None: # -> 단일 책임의 원칙에 따라 해당 내용은 분리되어야할듯...
            config = self.get_connection(self._conn_id)
            schema = config.schema or self.DEFAULT_SCHEMA
            host = config.host or self.DEFAULT_HOST
            port = config.port or self.DEFAULT_PORT

            self.base_url = f"{schema}//{host}:{port}"

            self.session = Session()

        if config.login: 
            self.session.auth = (config.login, config.password)

        return self.session, self.base_url



    
    def _get_with_paginations(self, endpoint, params, batch_size=100):
        session, base_url = self.get_conn()

        offset = 0
        total = None
        while total is None or offset < total:
            response = session.get(base_url,params={ **params,**{"offset":offset, "limit":batch_size}})
            response.raise_for_status()
            response_json = response.json()

            yield from response_json["result"]

            offset += batch_size
            total = response_json["total"]
    

    
    def get_ratings(self,start_date=None, end_date=None, batch_size=100):
        yield from self._get_with_paginations(endpoint= "/ratings",params={"start_date":start_date,"end_date":end_date},batch_size=batch_size)

    