from collections import Counter
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

def test_MakeRandomData():
    start = datetime(2023,5,30,15,14)
    end = datetime(2023,5,30,15,15)
    value = MakeRandomData(index_name="ips",start_date=start,end_date=end)


    test_value = {'UNKNOWN2': bytearray(b'q\x921\x07kb\xd4\x95SE'), 'SID': '2017143', 'UNKNOWN3': bytearray(b'!|\xfb\x03\xd9@<\xdd\xfb\x9a'), '@version': '1', 'tags': ['_grokparsefailure'], 'UNKNOWN1': bytearray(b'TD\x15\xf0\xbf\x1f\x94 \x88('), 'GID': '1', 'KUNKNOWN4': '7', 'd_port': '52025', 'tag': 'ips', 'snort': 'snort', 'descriptoin': '(http_inspect) NO CONTENT-LENGTH OR TRANSFER-ENCODING IN HTTP RESPONSE', 'class': ' Not Suspicious Traffic', 'priority': '2', 'protocol': 'TCP', 'event': {'original': '<9>1 2022-09-21T02:28:19.429156+09:00 pfSense.localdomain snort 66091 - - [1:2013504:3] ET POLICY GNU/Linux APT User-Agent Outbound likely related to package management [Classification: Not Suspicious Traffic] [Priority: 3] {TCP} 10.0.0.254:31686 -> 91.189.91.38:80'}, 'hostname': 'pfSense.localdomain', 's_port': '60287'}
    #print(value._change_original_log(test_value))
    print(value.make_data())

def test_GenerateLogDatas():
    test_params={
        "start_date" : datetime(2023,5,30,15,14),
        "end_date" : datetime(2023,5,30,15,15),
        "index_name": "ips",
        "size":10
    }
    
    test_obj = GenerateLogDatas(**test_params)
    print(test_obj.generate())


def test_GeneratorOperator():
    test_params={
        "start_date" : datetime(2023,5,30,15,14),
        "end_date" : datetime(2023,5,30,15,15),
        "index_name": "ips",
        "size":10,
        "conn_id":"docker_elastic"
    }
    GeneratorOperator(**test_params).execute()


if __name__ == "__main__":
    test_GeneratorOperator()
    #test_GenerateLogDatas()
    #test_MakeRandomData()
    # list_d = [{"test1":"test_v"},{"test2":"test_v"},{"test3":"test_v"}]
    # print(np.random.choice(list_d))
    pass
   #test_ConvertDataFrame()
    #test_MakeRadomDate()
    #test_MakeRandomIP()
    #test_AddSampleLogOperator()
    #test_RedisSensorOperaotr()