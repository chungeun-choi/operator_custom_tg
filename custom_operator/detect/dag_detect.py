from detect.detect import DetectSensorOperator,UserDetectInput
from airflow import DAG
from datetime import datetime

CONNECTION = "docker_elastic"

test_obj= UserDetectInput(
    detection_target={
        "s_IP":"10.44.44.*"
    },
    frequency= 3,
    interval=3
)

with DAG(
    dag_id= "Detect_data_by_using_userInput",
    description= "사용자가 등록한 특정 문자열이 데이터웨어하우스에서 조회 되었을 경우 탐지하고 알림 및 다음 액션을 진행하는 dag입니다",
    catchup=False,
    tags=["detecttor"],
    start_date =datetime(2022,5,28)
) as dag :
    detect_target_task = DetectSensorOperator(
        task_id = "Detect_target_",
        conn_id=CONNECTION,
        input=test_obj

    )

    detect_target_task
