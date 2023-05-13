import sys
sys.path.append("/Users/cucuridas/Desktop/operator_custom_tg")
sys.path.append("/opt/airflow/dags")

from generator.generator import *


def test_sample_logs():
    assert SampleLogs("docker_elastic").check("test")


def test_insert_sample_logs():
    SampleLogs("docker_elastic").insert("data")


if __name__ == "__main__":
    #test_sample_logs()
    test_insert_sample_logs()
    
    pass