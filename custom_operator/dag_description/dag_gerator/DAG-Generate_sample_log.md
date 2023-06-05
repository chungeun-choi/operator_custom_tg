<style>
table {
  border-collapse: separate;
  border-spacing: 0;
  text-align: left;
  line-height: 1.5;
  border-top: 1px solid #ccc;
  border-left: 1px solid #ccc;
  margin : 20px 10px;
}
table th {
  width: 150px;
  padding: 10px;
  font-weight: bold;
  vertical-align: top;
  border-right: 1px solid #ccc;
  border-bottom: 1px solid #ccc;
  border-top: 1px solid #fff;
  border-left: 1px solid #fff;
  background: #eee;
}
table td {
  width: 350px;
  padding: 10px;
  vertical-align: top;
  border-right: 1px solid #ccc;
  border-bottom: 1px solid #ccc;
}
</style>

# DAG -  Generate_sample_log


## 내용
---

해당 DAG는 Elasticsearch에 적재되어진 sample log를 증분하기 위해 DATA를 생성하는 역할을 진행합니다다.

진행 프로젝트 내에서 데이터를 수집하기 어려울 때 존재하는 데이터의 유형을 늘려 데이터를 증분하기 위해 개발하였습니다

프로젝트 디렉토리 내에 ‘sample_log’에 데이터와 index template을 저장 후,Airflow 화면에서 “Variable” 값으로 초기화된 내용을 전달 받아 DAG가 실행되어지게 됩니다

</br>

## 사용법
---

### 1) Variable 값 정의
해당 ‘Variables’의 값은 'Insert_sample_log' 와 공유합니다.a
내용에서 설정해주어야할 Variable의 값은 'sample_log'와 'log_size'입니다

<img width="842" alt="generator_op" src="https://github.com/cucuridas/operator_custom_tg/assets/65060314/2e748dc2-b300-4500-b9a0-5d9069926d8e">

```c
1. 상단의 메뉴바에서 'Admin' 클릭
2. 'Admin' 하위 메뉴에서 'Variables' 클릭
3. '+' 버튼을 눌러 새롭게 생성, 'sample_log'가 생성되어져 있을 경우 수정 버튼을 눌러 변경
4. key, value를 통해 데이터 정의 *key의 이름은 'sample_log' 고정
```

### 2) Operator 객체 생성하여 파라미터 정의

- 각 operator 파라미터 내용 (BaseOperator 내용은 생략되어 있습니다)
 
| Operator name | description | parameter description |
| --- | --- | --- |
| RedisSensorOperator(BaseSensorOperator) | redis에 sample data가 존재하는지 확인하는 operator | index_name(str): 찾고자하는 sample 데이터 index 이름 |
| AddSampleLogOperator(BaseOperator) | redis에 sample data가 존재하지 않을 때 elasticsearch에서 조회 후 데이터 전처리하여 redis에 적재 | index_name(str): 찾고자하는 sample 데이터 index 이름 <br /> conn_id(str):‘connection’에 등록되어진 elasticsearch 연결 정보<br /> size(int): sample로 참고할 데이터의 양 |
| GeneratorOperator(BaseOperator) | redis에 적재되어진 index sample 데이터를 통해 데이터 증분 | index_name(str): 찾고자하는 sample 데이터 index 이름<br /> conn_id(str):‘connection’에 등록되어진 elasticsearch 연결 정보<br /> size(int): sample로 참고할 데이터의 양<br />start_date(datetime): 데이터 생성 시 랜덤으로 생성할 데이터의 시작시간<br /> end_date(datetime): 데이터 생성 시 랜덤으로 생성할 데이터의 종료시간 |

<br>

## TASK
---

<img width="937" alt="generato_task" src="https://github.com/cucuridas/operator_custom_tg/assets/65060314/e3bd6ff5-9baf-44a3-94a2-95fc65a4f723">

총 3개의 task를 가지고 있으며 각각의 task는 아래의 표를 참고

| task name | Using operator |
| --- | --- |
| Check_redis_sensor_to_{index name} | RedisSensorOperator(BaseSensorOperator) |
| Add_sample_data_from_{index name} | AddSampleLogOperator(BaseOperator) |
| Generate_log_from_{index name} | GeneratorOperator(BaseOperator) |