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
from datetime import timedelta
from datetime import datetime

class GeneratorOperator(BaseOperator):
    
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

    def __init__(self,index_name:str,size:int,conn_id,**kwargs):
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
        

    def execute(self, context: Context) -> Any:
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

class MakeGLog():
    def __init__(self,data,start_date,end_date):
        self_data=data
        self._start_date = start_date
        self._end_date = end_date
        

    def _make_radom_IP(self):
        if self._data.has_key("s_IP") and self._data.has_key("d_IP"):
            self._random_ip = MakeRandomIP.twice()
        else :
            self._random_ip = MakeRandomIP.single()


    def _make_random_date(self):
        self.random_date = MakeRandomDate.random_date(self._start_date,self._end_date)

    def _changeData():
        pass


class MakeRandomData():

    def __init__(self,data,start_date,end_date):
        self_data=data
        self._start_date = start_date
        self._end_date = end_date
        

    def _make_radom_IP(self):
        if self._data.has_key("s_IP") and self._data.has_key("d_IP"):
            self._random_ip = MakeRandomIP.twice()
        else :
            self._random_ip = MakeRandomIP.single()


    def _make_random_date(self):
        self.random_date = MakeRandomDate.random_date(self._start_date,self._end_date)

    def _changeData():
        pass

class MakeRandomDate:
    def random_date(start:datetime, end:datetime):
        """
        This function will return a random datetime between two datetime 
        objects.
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
    

