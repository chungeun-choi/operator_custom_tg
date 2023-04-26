from airflow.hooks.base import BaseHook
from elastic.config import ElasticConfig
from typing import Any
from elasticsearch import Elasticsearch

class ElasticsearchHook(BaseHook):
    
    def __init__(self, conn_id ,context=None):
        super().__init__(context)

        conn_value = self.get_connection(conn_id) or None
         
        self._host = conn_value.host or ElasticConfig.ELASTIC_HOST
        self._port = conn_value.port or ElasticConfig.ELASTIC_PORT

        if conn_value.login :
            self._basic_auth = ( conn_value.login, conn_value.password)

        self._session : Elasticsearch = None
        
    

    def get_conn(self) -> Elasticsearch:
    
        if self._session is None :
            self._session = Elasticsearch(
                hosts= self.get_url(),
            )

        if self._basic_auth:
            self._session.basic_auth = self._basic_auth


        return self._session 



    def get_url(self) -> str:
        url = f"{self._host}:{self._port}"

        return url 