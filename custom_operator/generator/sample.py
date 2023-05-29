from airflow.models import BaseOperator
from airflow.sensors.base import BaseSensorOperator
from airflow.utils.context import Context
from airflow.utils.decorators import apply_defaults
from typing import Any
from elastic.hook import ElasticsearchHook

from elastic.config import ElasticConfig
import logging,orjson
from elasticsearch import helpers
from airflow.exceptions import AirflowException
DEFALUT_PATH = '/opt/airflow/dags/sample_data/'

class CheckSensorOperator(BaseSensorOperator):
    template_fields = {"_log_name"}
    @apply_defaults
    def __init__(self,*,conn_id, log_name,context=None,**kwargs):
        super().__init__(**kwargs)
        self.conn= ElasticsearchHook(conn_id= conn_id or "local").get_conn()
        self._log_name = log_name
        self.smaple_data_path = DEFALUT_PATH+'{}.json'.format(log_name)

    def poke(self,context):
        if self.conn.indices.exists(index=self._log_name):
            self.conn.close()
            return False
        else:
            logging.warning("Sample data does not exist")
            self.conn.close()
            return True


        
class InsertOperator(BaseOperator):
    template_fields = {"_log_name"}
    
    @apply_defaults
    def __init__(self,conn_id,log_name,**kwargs):
        super().__init__(**kwargs)
        self.conn= ElasticsearchHook(conn_id= conn_id or "local").get_conn()
        self._log_name = log_name
        self.smaple_data_path = DEFALUT_PATH+'{}.json'.format(log_name)
    
    def execute(self, context: Context) -> Any:
        with open(self.smaple_data_path,'r') as file:
            sample_logs= file.read().splitlines()

            data = [orjson.loads(sample_log)  for sample_log in sample_logs ]

            helpers.bulk(self.conn, data)
            
            self.conn.close()


class MakeIndexOperator(BaseOperator):
    template_fields={"_index_name"}

    @apply_defaults
    def __init__(self,conn_id,index_name,**kwargs) -> None:
        super().__init__(**kwargs)
        self.conn= ElasticsearchHook(conn_id= conn_id or "local").get_conn()
        self._index_name = index_name
        self._index_template_path = DEFALUT_PATH+'index_template/{}_template.json'.format(index_name)
        self._index_ilm_path = DEFALUT_PATH+'ilm_template/{}_ilm.json'.format(index_name)

    def __call__(self) -> Any:
        self.make_index_with_all()

    def execute(self, context: Context) -> Any:
        self.make_index_with_all()
        self.conn.close()
        
    def make_index_with_all(self):
        '''
        해당 객체를 생성할 떄 사용한 변수들을 사용하여 elasticsearch index를 생성하기위한
        요소들을 정의하고 elasticsearch에 등록하는 작업을 합니다
        '''
        
        self.make_ilm_policy()
        self.make_index_template()
        self.make_index()

            #AirflowException("Error generating index for example data")

    def make_index(self):
        '''
        새로운 index를 만드는 함수입니다
        '''
        self.conn.indices.create(index=self._index_name)
        

    def make_ilm_policy(self):
        '''
        새로운 ilm policy 등록하는 함수입니다
        해당 객체를 생성할 떄 초기화된 path 정보를 바탕으로 json 파일을 읽어들여
        해당 내용으로 ilm policy 생성합니다
        '''
        with  open(self._index_ilm_path,'r') as file:
            policy_data = orjson.loads(file.read())
            print(policy_data)
            self.conn.ilm.put_lifecycle(policy=self._index_name,body=policy_data)


    def make_index_template(self):
        '''
        새로운 index template을 등록하는 함수입니다
        해당 객체를 생성할 떄 초기화된 path 정보를 바탕으로 json 파일을 읽어들여
        해당 내용으로 index template을 생성합니다
        '''
        with  open(self._index_template_path,'r') as file:
            template_data = orjson.loads(file.read())
            print(template_data)
            self.conn.indices.put_index_template(name='{}_tempalte'.format(self._index_name),body=template_data)
            