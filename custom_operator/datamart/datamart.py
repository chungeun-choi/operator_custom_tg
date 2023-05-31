from typing import Union
from airflow.models import BaseOperator
from elastic.hook import ElasticsearchHook
from airflow.utils.context import Context
from airflow.exceptions import AirflowException

class UserInput:
    #index_name,type,query(dsl, sql), data_mart 이름,저장방식
    index_name: str
    query_type: str 
    query: Union[str,dict]
    datamart_name: str
    save_type: str




class MakeDataMartOperator(BaseOperator):
    def __init__(self,input:UserInput,conn_id:str = None,**kwargs):
        self._input = input
        self._es_conn = ElasticsearchHook(conn_id= conn_id or "local").get_conn()
        self._save_type = "json" if input.save_type == "datawarehouse" else input.save_type

    def _save(self):
        if self._save_type =="csv":
            pass
        elif self._save_type == "dataWarehouse":
            pass
        else:
            AirflowException("Does not support")

    def _make_index(self):
        pass

    def _make_csv(self):
        pass

    def _get_data(self):
        if self._input.query_type == "sql":
            result = self._es_conn.sql.query(self._input.query,format=self._save_type)
        else:
            result = self._es_conn.search(index=self._input.index_name,body=self._input.query)
        
        return result

    def execute(self,context:Context):

        result = self._get_data()
        self._save(result)
    


    