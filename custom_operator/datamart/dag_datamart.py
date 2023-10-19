from datamart.datamart import UserInput, MakeDataMartOperator, SaveElasticsearchOperator
from airflow import DAG
from datetime import datetime
from airflow.models.param import Param
from path import DEFAULT_PATH
from airflow.exceptions import AirflowException
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.operators.email import EmailOperator
import pandas, orjson, os


CONNECTION = "docker_elastic"
# LOG_NAME = Variable.get("sample_log",deserialize_json=True)
DESCRIPTION = """"""

with open(
    DEFAULT_PATH + "/dag_description/dag_datamart/DAG-Make_datamart.md", "r"
) as file:
    DESCRIPTION = file.read()


def get_run_task(params, **kwags):
    if params["save_type"] == "csv":
        return "make_csv_file"
    elif params["save_type"] == "warehouse":
        return "save_elasticsearch_task"
    else:
        AirflowException("Does not supported value")


def make_csv(params, **context):
    text = context["task_instance"].xcom_pull(task_ids="make_data_mart_task")
    data = pandas.DataFrame(orjson.loads(text))
    data.to_csv(DEFAULT_PATH + "{}.csv".format(params["datamart_name"]))


def remove_csv(params, **context):
    os.remove(DEFAULT_PATH + "{}.csv".format(params["datamart_name"]))


with DAG(
    dag_id="Make_datamart",
    tags=["datamart"],
    doc_md=DESCRIPTION,
    description="Varilable에 정의되어진 정보를 통해 dat datawarehouse에서 data mart를 생성하는 DAG입니다",
    start_date=datetime(2022, 5, 28),
    catchup=False,
    params={
        # an int with a default value
        "index_name": Param(
            "iis_log", description="찾고자 하는 값이 존재하는 Index의 이름입니다", type="string"
        ),
        "query_type": Param("sql", enum=["sql", "dsl"]),
        # an enum param, must be one of three values
        "query": Param(
            "SELECT s_IP,count(*) FROM iis_log GROUP BY s_IP HAVING count(*) > 10",
            type=["array", "string"],
        ),
        "datamart_name": Param("data_mart_iis_log_rule1", type="string"),
        "save_type": Param("warehouse", enum=["csv", "warehouse", "dataframe"]),
        "email": Param(None, description="save_type이 csv일 경우 전달 받기 위한 이메일을 정의해야합니다")
        # a param which uses json-schema formatting
    },
    render_template_as_native_obj=False,
) as dag:
    make_datamart_task = MakeDataMartOperator(
        task_id="make_data_mart_task", input=UserInput(**dag.params), conn_id=CONNECTION
    )
    check_save_type = BranchPythonOperator(
        task_id="check_save_type", python_callable=get_run_task
    )
    save_elasticsearch_task = SaveElasticsearchOperator(
        task_id="save_elasticsearch_task",
        data_mart_name=dag.params["datamart_name"],
        conn_id=CONNECTION,
        prev_task_id="make_data_mart_task",
    )
    save_csv_task = PythonOperator(task_id="make_csv_file", python_callable=make_csv)

    send_csv_task = EmailOperator(
        task_id="send_email_with_datamart_csv",
        to="3310223@naver.com",
        subject="데이터 마트 - {}".format(dag.params["datamart_name"]),
        html_content="Airflow를 통해 작성한 정책을 통해 생성되어진 데이터 마트 csv 파일입니다",
        files=[DEFAULT_PATH + "{}.csv".format(dag.params["datamart_name"])],
    )

    delete_csv_task = PythonOperator(
        task_id="delete_csv_file",
        python_callable=remove_csv,
        trigger_rule="one_success",
    )

    make_datamart_task >> check_save_type >> [save_elasticsearch_task, save_csv_task]
    save_csv_task >> send_csv_task >> delete_csv_task
