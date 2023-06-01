from datamart.datamart import UserInput, MakeDataMartOperator
from airflow import DAG 
from datetime import datetime
from airflow.models.variable import Variable
from airflow.utils.task_group import TaskGroup


CONNECTION = "docker_elastic"
#LOG_NAME = Variable.get("sample_log",deserialize_json=True)

test=UserInput(...)

with DAG(
    dag_id="Make_datamart",
    tags=["datamart"],
    description="Varilable에 정의되어진 정보를 통해 dat awarehouse에서 data mart를 생성하는 DAG입니다",
    start_date = datetime(2022,5,28),
) as dag:
    make_datamart_task = MakeDataMartOperator(
        task_id ="make_data_task_",
        input = test,
        conn_id=CONNECTION
    )