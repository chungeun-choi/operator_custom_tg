from generator.generator import GeneratorOperator,RedisSensorOperator,AddSampleLogOperator
from airflow import DAG 
from datetime import datetime
from airflow.models.variable import Variable
from airflow.utils.task_group import TaskGroup
from path import DEFAULT_PATH

CONNECTION = "docker_elastic"
LOG_NAME = Variable.get("sample_log",deserialize_json=True)

DESCRIPTION = ''''''

with open(DEFAULT_PATH+"/dag_description/dag_gerator/DAG-Generate_sample_log.md","r") as file:
    DESCRIPTION = file.read()

with DAG(
    dag_id = "Generate_sample_log",
    doc_md = DESCRIPTION,
    description="redis에 적재되어진 sample log 데이터를 통해서 log 데이터를 새로 생성하여 증분합니다",
    #schedule="@minute"
    #schedule_interval="@dayily",
    catchup=False,
    tags=["generator"],
    start_date =datetime(2022,5,28)
) as dag :
    for log in LOG_NAME:
        with TaskGroup(group_id='Group_{}'.format(log)) as innserGroup:

            redis_sensor_task = RedisSensorOperator(
                task_id = "Check_redis_sensor_to_{}".format(log),
                index_name= log,
                timeout= 10,
                soft_fail=True
            )

            add_sample_task = AddSampleLogOperator(
                task_id =  "Add_sample_data_from_{}".format(log),
                index_name= log,
                size= 10000,
                conn_id=CONNECTION,
                trigger_rule="all_success"
            ) 

            generate_log_task = GeneratorOperator(
                task_id = "Generate_log_from_{}".format(log),
                index_name = log,
                size=10,
                conn_id=CONNECTION,
                trigger_rule="none_failed",
                start_date=datetime.fromisoformat('{{execution_date}}'),
                end_date=datetime.fromisoformat("{{next_execution_date}}")
            )

        redis_sensor_task >> add_sample_task
        add_sample_task >> generate_log_task
