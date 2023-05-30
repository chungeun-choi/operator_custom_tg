import sys
sys.path.append("/Users/cucuridas/Desktop/operator_custom_tg")
sys.path.append("/opt/airflow/dags")

from generator.generator import *
from datetime import datetime




def test_RedisSensorOperaotr():
    test_obj = RedisSensorOperator(index_name="firewall")
    #test_obj.conn.set("sample_firewall","test")
    assert test_obj.poke(context=None)
    

def test_AddSampleLogOperator():
    test_obj = AddSampleLogOperator(index_name="ips",size=10000,conn_id="docker_elastic")
    test_obj.execute(context=None)


def test_MakeRandomIP():
    test_obj = MakeRandomIP.twice()
    print(test_obj)

def test_MakeRadomDate():
    start = datetime(2023,5,30,15,14)
    end = datetime(2023,5,30,15,15)
    test_obj = MakeRandomDate.random_date(start,end)

    print(test_obj)

def test_ConvertDataFrame():
    
    mockup_obj = AddSampleLogOperator(index_name="ips",size=10000,conn_id="docker_elastic")
    data = mockup_obj._get_sample_data_from_es()

    test_obj = ConvertDataFrame(data)
    print(test_obj.extract_case())

if __name__ == "__main__":
    pass
   #test_ConvertDataFrame()
    #test_MakeRadomDate()
    #test_MakeRandomIP()
    #test_AddSampleLogOperator()
    #test_RedisSensorOperaotr()