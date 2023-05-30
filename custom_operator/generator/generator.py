import os
from typing import Any
from airflow.models import BaseOperator
from airflow.sensors.base import BaseSensorOperator, PokeReturnValue
from airflow.utils.context import Context
from elastic.hook import ElasticsearchHook
from airflow.utils.decorators import apply_defaults
from airflow.hooks.base import BaseHook
import redis
from airflow.models.connection import Connection
import orjson,socket,random,struct,pandas
from random import randrange
from datetime import timedelta,datetime
import numpy as np

class GeneratorOperator(BaseOperator):
    def __init__(self,index_name:str,size:int,start_date:datetime,end_date:datetime,conn_id:str,**kwargs):
        super().__init__(**kwargs)
        self._created_data = GenerateLogDatas(size=size,index_name=index_name,start_date=start_date,end_date=end_date)
        self.es_conn = ElasticsearchHook(conn_id= conn_id or "local").get_conn()
        
    def execute(self):
        #self.es_conn.bulk
        pass


class RedisHook(BaseHook):
    def __init__(self,db:int=None):
        try:
            self.conn_info =  BaseHook.get_connection(conn_id="redis")

        except: 
            self.conn_info = Connection(conn_id="redis",host="operator_custom_tg-redis-1",port=6379)
        
        self._db = db

    def get_conn(self):
        '''
        redis와 연결하기위한 연결 객체를 만듭니다
        '''
        self.conn = redis.Redis(host=self.conn_info.host, port=self.conn_info.port, db=self._db or 0,decode_responses=True)
        return self.conn
    

class RedisSensorOperator(BaseSensorOperator):
    '''
    Redis에 참조할 sample log가 적재되었는지 확인하기 위한 sensor operator입니다
    '''
    template_fields = {"_index_name"}

    @apply_defaults
    def __init__(self,index_name:str,**kwargs):
        '''
        
        '''
        #super().__init__(**kwargs)
        self._index_name = index_name
        self.conn = RedisHook(db=1).get_conn()
    

    def poke(self, context: Context) :
        '''
        sample data를 확인하기위한 poke 함수를 정의합니다
        sample data가 미존재시 True를 반환합니다
        '''
        sample_data = self.conn.get("sample_{}".format(self._index_name))
        if sample_data is None:
            return True
        else:
            return False





class AddSampleLogOperator(BaseOperator):
    '''
    redis에 적재되어진 sample 데이터가 없을 경우 elasticsearch에서 데이터를 가져와
    적재합니다
    '''

    def __init__(self,index_name:str,size:int,conn_id,**kwargs):
        '''
        params:
            index_name(str): elasticsearch index 이름,
            size(int): sample 데이터의 양
            conn_id(str): elasticsearch conntion 정보를 가져올 id
        '''
        #super().__init__(**kwargs)
        self._index_name = index_name
        self._size = size
        self.es_conn = ElasticsearchHook(conn_id= conn_id or "local").get_conn()
        self.redis_conn = RedisHook(db=1).get_conn()
        
    def _get_sample_data_from_es(self):
        sample = self.es_conn.search(index=self._index_name,body={},size=self._size)
        
        return sample["hits"]["hits"]

    def _preprocess_sample_data(self,data):
        key_list = list(data[0]["_source"].keys())
        preprocess_data = {"key_list":key_list}

        case_data = ConvertDataFrame(data).extract_case()
        preprocess_data.setdefault("case_data",case_data)

        return preprocess_data

    def _insert_sample_data_to_reids(self,data):
        self.redis_conn.set("sampe_{}".format(self._index_name),data)
        

    def execute(self, context: Context) :
        '''
        operator 객체를 생성하고 task를 execute하는 함수
        '''
        get_data = self._get_sample_data_from_es()
        sample_case_data = self._preprocess_sample_data(get_data)
        self._insert_sample_data_to_reids(orjson.dumps(sample_case_data))

class ConvertDataFrame():
    def __init__(self,data):
        source_list = list(map(lambda x:x["_source"],data))
        self._convert_data = pandas.DataFrame.from_records(source_list)


    def extract_case(self):
        fileds = self._convert_data.columns
        case_data = {}
        
        
        for filed in fileds :
            if filed in ("_index","_id","s_IP","d_IP","@timestamp") or filed.startswith("UNKNOWN"):
                continue
            else:
                case_data.setdefault(filed,self._convert_data[filed].drop_duplicates().to_list())
        
        return case_data


      
        
class MakeRandomData():

    def __init__(self,index_name:str,start_date:datetime,end_date:datetime):
        self._index_name = index_name
        self._redis_sample = RedisHook(1).get_conn().get("sampe_{}".format(self._index_name))
        self._start_date = start_date
        self._end_date = end_date       

    def make_data(self)->dict:
        '''
        해당 클래스내의 내장 함수를 통해 랜덤 데이터를 생성합니다
        랜덤 데이터 생성 시 reids에 적재되어진 sample 내용을 참조하여 생성하게됩니다
        '''
        self._make_radom_IP()
        self._make_random_date()
        return self._changeData()

    def _make_radom_IP(self):
        if "s_IP" in self._redis_sample["key_list"] and "d_IP" in self._redis_sample["key_list"]:
            self._random_ip = MakeRandomIP.twice()
        else :
            self._random_ip = MakeRandomIP.single()


    def _make_random_date(self):
        self.random_date = MakeRandomDate.random_date(self._start_date,self._end_date)

    def _changeData(self):
        data = {}
        for field in self._redis_sample["key_list"]:
            if field.startswith("UNKNOWN"):
                data.setdefault(field,bytearray(os.urandom(1000000)))
            elif field in ("_index","_id","s_IP","d_IP","@timestamp"):
                continue
            else:
                random_value = np.random.choice(self._redis_sample["case_data"][field], size=1)
                data.setdefault(field,random_value)
        return data
        
class GenerateLogDatas(MakeRandomData):
    def __init__(self,size,**kwargs):
        self._size = size
        super().__init__(**kwargs)
        
    def generate(self):
        
        generate_log = [self._changeData() for count in range(self._size)]
        
        return generate_log
        
        
        
class MakeRandomDate:
    def random_date(start:datetime, end:datetime):
        """
        시작날짜와 종료날짜를 입력받아 랜덤한 날짜를 전달하는 함수입니다
        """
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)

class MakeRandomIP:
    def single()->str:
        random_ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        return random_ip

    def twice()->list:

        random_ip = []
        for i in range(2):
            random_ip.append(socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))))
        return random_ip
    

