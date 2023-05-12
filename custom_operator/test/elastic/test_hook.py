import sys
sys.path.append("/Users/cucuridas/Desktop/operator_custom_tg")
sys.path.append("/opt/airflow/dags")
from elastic.hook import ElasticsearchHook



def test_connection():
    test_obj = ElasticsearchHook("docker_elastic")
    test_obj.get_conn()
    test_obj._session.ping()

if __name__ == "__main__":
    test_connection()