from typing import Union
from airflow.models import BaseOperator
from elastic.hook import ElasticsearchHook
from airflow.utils.context import Context
from airflow.exceptions import AirflowException
import pandas
from generator.generator import create_id
from elasticsearch import helpers

class UserInput:
    #index_name,type,query(dsl, sql), data_mart 이름,저장방식
    def __init__(self,
    index_name: str,
    query_type: str ,
    query: Union[str,dict],
    datamart_name: str,
    save_type: str,
    ):
        self._index_name = index_name
        self._query_type = query_type
        self._query = query
        self._datamart_name = datamart_name
        self._save_type = save_type




class MakeDataMartOperator(BaseOperator):
    def __init__(self,input:UserInput,conn_id:str = None,**kwargs):
        self._input = input
        self._es_conn = ElasticsearchHook(conn_id= conn_id or "local").get_conn()
        self._save_type = "json" if input._save_type == "warehouse" else input._save_type

    def _save(self):
        if self._save_type =="csv":
            self._make_csv()
        elif self._save_type == "warehouse":
            self._make_index()
        elif self._save_type == "warehouse":
            self._make_dataframe()
        else:
            AirflowException("Does not support")

    def _make_index(self):
        json_datas = self._convert_dataframe().to_json()
        index_rows = [{"_index": self._input._datamart_name, "_id": create_id(19), "_source": data} for data in json_datas]
        
        helpers.bulk(self._es_conn, index_rows)

    def _make_csv(self):
        self._convert_dataframe()
        self.convert_data.to_csv("./{}.csv".format(self._input._datamart_name))
        
    def _make_dataframe(self):
        return self._convert_dataframe()


    def _convert_dataframe(self):
        data = self.result
        if "columns" in data:
            columns_list = list(map(lambda x: x["name"],data["columns"]))
            self.convert_data = pandas.DataFrame.from_records(columns=columns_list,data=data["rows"])
            #self.convert_data = pandas.DataFrame.from_records(columns=data["columns"],data=data["rows"])
            return self.convert_data
        else :
            hits = data["hits"]["hits"]
            row_list = list(map(lambda x:x["_source"],hits))

            self.convert_data = pandas.DataFrame.from_records(row_list)
            return self.convert_data

    def get_data(self):
        if self._input._query_type == "sql":
            body =  {"query": self._input._query}
            self.result = self._es_conn.sql.query(body=body)
        else:
            self.result = self._es_conn.search(index=self._input._index_name,body=self._input._query)
        
        return self.result

    def execute(self,context:Context):

        self.get_data()
        self._save()
    


    