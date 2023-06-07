import logging
from typing import Union
from airflow.models import BaseOperator
from elastic.hook import ElasticsearchHook
from airflow.utils.context import Context
from airflow.exceptions import AirflowException
import pandas, orjson, json
from generator.generator import create_id
from airflow.utils.decorators import apply_defaults
from elasticsearch import helpers
from datetime import datetime
from typing import Optional


class UserInput:
    # index_name,type,query(dsl, sql), data_mart 이름,저장방식
    def __init__(
        self,
        query_type: str,
        query: Union[str, dict],
        datamart_name: str,
        save_type: str,
        email: Optional[str] = None,
        index_name: Optional[str] = None,
    ):
        self._index_name = index_name
        self._query_type = query_type
        self._query = query
        self._datamart_name = datamart_name
        self._save_type = save_type
        if save_type == "csv" and email == None:
            AirflowException(
                "Email information is required if 'save_type' is 'csv'. Define the parameter value using the 'email' key"
            )


class MakeDataMartOperator(BaseOperator):
    @apply_defaults
    def __init__(self, input: UserInput, conn_id: str = None, **kwargs):
        super().__init__(**kwargs)
        self._input = input
        self._es_conn = ElasticsearchHook(conn_id=conn_id or "local").get_conn()
        self._save_type = input._save_type

    def _make_csv(self):
        self._convert_dataframe()
        self.convert_data.to_csv("./{}.csv".format(self._input._datamart_name))

    def _convert_dataframe(self):
        data = self.result
        if "columns" in data:
            columns_list = list(map(lambda x: x["name"], data["columns"]))
            self.convert_data = pandas.DataFrame.from_records(
                columns=columns_list, data=data["rows"]
            )
            # self.convert_data = pandas.DataFrame.from_records(columns=data["columns"],data=data["rows"])
            return self.convert_data
        else:
            hits = data["hits"]["hits"]
            row_list = list(map(lambda x: x["_source"], hits))

            self.convert_data = pandas.DataFrame.from_records(row_list)
            return self.convert_data

    def get_data(self):
        if self._input._query_type == "sql":
            body = {"query": self._input._query}
            self.result = self._es_conn.sql.query(body=body)
        else:
            self.result = self._es_conn.search(
                index=self._input._index_name, body=self._input._query
            )

        return self.result

    def execute(self, context: Context):
        self.get_data()
        return self._convert_dataframe().to_json()


class SaveElasticsearchOperator(BaseOperator):
    def __init__(
        self,
        data_mart_name,
        conn_id: str = None,
        date: datetime = None,
        prev_task_id: str = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._es_conn = ElasticsearchHook(conn_id=conn_id or "local").get_conn()
        self._task_id = prev_task_id
        self._data_mart = data_mart_name
        self._datetime = date

    def _make_index(self, dataframe: json):
        data = pandas.DataFrame(orjson.loads(dataframe))
        json_datas = data.to_json(orient="records")
        if json_datas is not None:
            insert_data = orjson.loads(json_datas)
        index_rows = [
            {"_index": self._data_mart, "_id": create_id(19), "_source": data}
            for data in insert_data
        ]

        helpers.bulk(self._es_conn, index_rows)

    def execute(self, context: Context):
        text = context["task_instance"].xcom_pull(task_ids=self._task_id)
        # print("이거 타입",type(text))
        self._make_index(
            dataframe=text,
        )
