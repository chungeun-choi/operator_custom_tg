from datamart.datamart import UserInput, MakeDataMartOperator
from airflow import DAG 
from datetime import datetime
from airflow.models.variable import Variable
from airflow.utils.task_group import TaskGroup
from path import DEFAULT_PATH

CONNECTION = "docker_elastic"
#LOG_NAME = Variable.get("sample_log",deserialize_json=True)
DESCRIPTION = ''''''

with open(DEFAULT_PATH+"/dag_description/dag_datamart/DAG-Make_datamart.md","r") as file:
    DESCRIPTION = file.read()



TEST_OBJ = UserInput(
    index_name="waf",
    query_type="sql",
    query="SELECT * FROM waf",
    datamart_name="test_obj_sql_1",
    save_type="warehouse"
)




with DAG(
    dag_id="Make_datamart",
    tags=["datamart"],
    doc_md = DESCRIPTION,
    description="Varilable에 정의되어진 정보를 통해 dat awarehouse에서 data mart를 생성하는 DAG입니다",
    start_date = datetime(2022,5,28),
    catchup=False
) as dag:
    make_datamart_task = MakeDataMartOperator(
        task_id ="make_data_task_",
        input = TEST_OBJ,
        conn_id=CONNECTION
    )

make_datamart_task