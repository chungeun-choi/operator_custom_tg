from datamart.datamart import UserInput, MakeDataMartOperator, SaveElasticsearchOperator
from airflow import DAG
from datetime import datetime
from airflow.models.variable import Variable
from airflow.utils.task_group import TaskGroup
from airflow.models.param import Param
from path import DEFAULT_PATH

CONNECTION = "docker_elastic"
# LOG_NAME = Variable.get("sample_log",deserialize_json=True)
DESCRIPTION = """"""

with open(
    DEFAULT_PATH + "/dag_description/dag_datamart/DAG-Make_datamart_scheduling.md", "r"
) as file:
    DESCRIPTION = file.read()


with DAG(
    dag_id="Make_datamart_by_scheduling",
    tags=["datamart"],
    doc_md=DESCRIPTION,
    description="Varilable에 정의되어진 정보를 통해 dat awarehouse에서 data mart를 생성하는 DAG입니다 스케쥴링되어 작업이 진행됩니다",
    start_date=datetime(2022, 5, 28),
    schedule_interval="*/1 * * * *",
    catchup=False,
    params={
        "index_name": Param(
            "iis_log", description="찾고자 하는 값이 존재하는 Index의 이름입니다", type="string"
        ),
        "query_type": Param("dsl", enum=["sql", "dsl"]),
        "query": Param("foo", type=["array", "string"]),
        "datamart_name": Param("data_mart_iis_log_rule1", type="string"),
    },
) as dag:
    for value in Variable.get("datamart_lsit", deserialize_json=True):
        make_datamart_task = MakeDataMartOperator(
            task_id="make_data_task_{}".format(value["datamart_name"]),
            input=UserInput(save_type="warehouse", **value),
            conn_id=CONNECTION,
        )

        save_elasticsearch_task = SaveElasticsearchOperator(
            task_id="save_elasticsearch_task",
            conn_id=CONNECTION,
            prev_task_id="make_data_task_{}".format(value["datamart_name"]),
            data_mart_name=value["datamart_name"],
        )

    make_datamart_task >> save_elasticsearch_task
