from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException
from airflow.utils.context import Context
from airflow.sensors.base import BaseSensorOperator
from elastic.hook import ElasticsearchHook
import orjson


class UserDetectInput:
    def __init__(self, detection_target: dict, frequency: int, interval):
        self._detection_target = detection_target
        self._frequency = frequency
        self._interval = interval


class DetectSensorOperator(BaseSensorOperator):
    def __init__(self, conn_id: str, input: UserDetectInput, **kwargs):

        kwargs["poke_interval"] = 60
        kwargs["max_wait"] = input._interval * 60

        super().__init__(**kwargs)

        self._conn_id = conn_id
        self._input = input
        self.es_conn = ElasticsearchHook(conn_id=conn_id or "local").get_conn()
        self.count = 0

    def search_doc(self):
        with open("./detect_query.json", "r") as file:
            body = orjson.loads(file)
            result = self.es_conn.search(body=body)

            if result["hits"]["hits"] is not None:
                self.count + 1

    def poke(self, context: Context):
        if self.count == self._input._frequency:
            return True
        else:
            self.search_doc()
            return False
