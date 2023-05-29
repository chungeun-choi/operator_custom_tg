import sys
sys.path.append("/Users/cucuridas/Desktop/operator_custom_tg")
sys.path.append("/opt/airflow/dags")

from generator.sample import *


def test_sample_logs():
    assert SampleLogs("docker_elastic").check("test")


def test_insert_sample_logs():
    SampleLogs("docker_elastic","ips").insert()

def test_make_index_obj():
    MakeIndex("docker_elastic","firewall")()

if __name__ == "__main__":
    #test_sample_logs()
    #test_insert_sample_logs()
    # test_make_ilm_polity()
    # test_index_template()
    #test_make_index_obj()
    print( SampleLogs("docker_elastic","waf").check())