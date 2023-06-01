from generator.sample import CheckSensorOperator,MakeIndexOperator,InsertOperator
from airflow import DAG 
from datetime import datetime
from airflow.models.variable import Variable
from airflow.utils.task_group import TaskGroup


CONNECTION = "docker_elastic"
LOG_NAME = Variable.get("sample_log",deserialize_json=True)


with DAG(
    dag_id="Insert_sample_log",
    tags=["sample"],
    description="해당 DAG는 실행 시 최초에만 실행되면 Sample Log의 존재 유무를 판별하는 DAG입니다",
    schedule="@once",
    start_date = datetime(2022,5,28),
) as dag:
    
    for log in LOG_NAME:
        with TaskGroup(group_id='Group_{}'.format(log)) as innerGroup:
            check_sample_log = CheckSensorOperator(
                task_id= "check_sensor_task_{}".format(log),
                conn_id=CONNECTION,
                log_name=log,
                timeout = 10,
                soft_fail=True
            )
            make_index= MakeIndexOperator(
                task_id= "make_index_{}".format(log),
                conn_id=CONNECTION,
                trigger_rule ="all_success" ,
                index_name=log
            )
            insert_sample_data = InsertOperator(
                task_id="insert_sample_data_{}".format(log),
                conn_id=CONNECTION,
                log_name=log,
                trigger_rule = "none_failed"
        )

        check_sample_log >> make_index >> insert_sample_data



