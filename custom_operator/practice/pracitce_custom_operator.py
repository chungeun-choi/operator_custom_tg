from airflow.models import BaseOperator
from airflow.utils.context import Context
from airflow.utils.decorators import apply_defaults
from typing import Any
from custom_operator.practice.pracitce_custom_hook import MovielensHook
import os, json

# DAG에서 호출하여 사용하기위한 custom operator를 정의합니다 기본적으로 BaseOperator를 상속받아 생성됩니다
class MovielensFetchRatingsOperator(BaseOperator):
    template_fields = ("_start_date","_end_date","_output_path")
    @apply_defaults
    def __init__(self,conn_id,output_path,start_date,end_date,**kwargs):
        super(MovielensFetchRatingsOperator,self).__init__(**kwargs)

        self._conn_id = conn_id
        self._output_path = output_path
        self._start_date = start_date
        self._end_date = end_date
    
    # 해당 operator의 기능은 시작 날짜(start_date)와 종료 날짜(end_date)를 입력받아 해당 날짜의 영화 순위 데이터를 받아옵니다
    # 이전에 생성했던 MovielensHook 을 통해 연결 객체를 얻고 내부 함수인 get_ratings 함수를 통해 데이터를 Fecth하는 작업을 진행합니다
    def execute(self, context: Context) -> Any:

        hook = MovielensHook(self._conn_id)

        try: 
            self.log.info(
                f"Fetching ratings for {self._start_date} to {self._end_date}"
            )
            ratings = list(
                hook.get_ratings(
                start_date=self._start_date,
                end_date=self._end_date,
                )
            )
            self.log.info(f"Fetched {len(ratings)} ratings")
        finally:
            hook.close()
        
        self.log.info(f"Writing ratings to {self._output_path}")

        output_dir = os.path.dirname(self)
        os.makedirs(output_dir,exist_ok=True)

        with open(self._output_path,"w") as file_:
            json.dump(ratings, fp=file_)

        




    