from airflow.models import BaseOperator
from airflow.utils.context import Context
from airflow.utils.decorators import apply_defaults
from typing import Any
from elastic.hook import ElasticsearchHook
from elastic.config import ElasticConfig
import logging,orjson
from elasticsearch import helpers


class SampleLogs(ElasticsearchHook):
    def __init__(self,conn_id) -> None:
        
        self.conn= ElasticsearchHook(conn_id= conn_id or "local").get_conn()

    def check(self,log_name: str):
        try :
            self.conn.search(index=log_name)
        except:
            logging.warning("Sample data does not exist")
            self.insert(ElasticConfig.SAMPLE_DATA)

            
    def insert(self,file_path: str):
        with open(file_path,'r') as file:
            sampel_datas = orjson.loads(file)
            
        pass

    def make_index():
        pass

class GenerateLogOperator(BaseOperator):
    #template__fields = ("")

    @apply_defaults
    def __init__(self,**kwargs):
        super(GenerateLogOperator,self).__init__(**kwargs)



    def execute(self, context: Context) -> Any:
        return super().execute(context)