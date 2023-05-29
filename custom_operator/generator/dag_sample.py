from generator.sample import CheckSensorOperator,MakeIndexOperator,InsertOperator
from airflow import DAG 
from datetime import datetime
from airflow.sensors.python import PythonSensor


CONNECTION = "docker_elastic"
LOG_NAME = "ips"


with DAG(
    dag_id="Sample_Log",
    description="해당 DAG는 실행 시 최초에만 실행되면 Sample Log의 존재 유무를 판별하는 DAG입니다",
    schedule="@once",
    start_date = datetime(2022,5,28),
) as dag:
    check_sample_log = CheckSensorOperator(
        task_id= "check_sensor_task",
        conn_id=CONNECTION,
        log_name=LOG_NAME
    )
    make_index= MakeIndexOperator(
        task_id= "make_index",
        conn_id=CONNECTION,
        index_name=LOG_NAME
    )
    insert_sample_data = InsertOperator(
        task_id="insert_sample_data",
        conn_id=CONNECTION,
        log_name=LOG_NAME
    )



check_sample_log >> make_index >> insert_sample_data
