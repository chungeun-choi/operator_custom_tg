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


# DAG -  Insert_sample_log

## 내용
---

해당 DAG는 Elasticsearch에 적재되어진 sample log가 존재하지 않을 경우 프로젝트 디렉토리(./sample_data)의 json 형태의 데이터를 elasticsearch에 적재하는 역할을 하는 DAG 입니다

프로젝트 초반 환경 이전이 잦아 해당 DAG를 개발하여 진행하였습니다

- 디렉토리 설명

| directory name | description |
| --- | --- |
| ilm_template | elasticsearch ILM(Index LifeCyclt Management) 설정과 관련되어진 내용이 정리되어진 json파일이 존재합니다 |
| index_template | 데이터(document)를 적재하기 전 index를 정의하는 역할을 하는 설정 내용이 담긴 json 파일입니다 |

</br>

## 사용법
---

### 1) sample 데이터 추가

‘내용’ 에서 설명했듯이 로젝트 디렉토리(./sample_data)에 저장되어진 데이터 파일(json)을 사용하여 sample 데이터를 추가함에 따라 데이터에 대한 내용을 추가해주어야합니다 

```c
rows data -> './sample_data' 내에 json 형태,파일 이름 {index name}.json 포맷으로 추가
index template configure file -> './sample_data/index_template' 내에 파일 이름 {index name}template.json 포맷으로 추가 
ilm template configure file -> './sample_data/il_template' 내에 파일 이름 {index name}_ilm.json 포맷으로 추가 
```

### 2) Variable 값 정의

해당 ‘Variables’의 값은 ‘Generate_sample_log’ 와 공유합니다

<img width="842" alt="generator_op" src="https://github.com/cucuridas/operator_custom_tg/assets/65060314/2e748dc2-b300-4500-b9a0-5d9069926d8e">


```c
1. 상단의 메뉴바에서 'Admin' 클릭
2. 'Admin' 하위 메뉴에서 'Variables' 클릭
3. '+' 버튼을 눌러 새롭게 생성, 'sample_log'가 생성되어져 있을 경우 수정 버튼을 눌러 변경
4. key, value를 통해 데이터 정의 *key의 이름은 'sample_log' 고정
```

### 3) Operator 객체 생성하여 파라미터 정의

- 각 operator 파라미터 내용 (BaseOperator 내용은 생략되어 있습니다)

| Operator name | description | parameter description |
| --- | --- | --- |
| CheckSensorOperator(BaseSensorOperator) | Elasticsearch 에 ‘Variables’의 index_list에 설정한 index가 존재하는 지 확인하는 sensoroperator  | log_name(str): 찾고자하는 sample 데이터 index 이름 <br /> conn_id(str):‘connection’에 등록되어진 elasticsearch 연결 정보 |
| MakeIndexOperator(BaseOperator) | CheckSensorOperator(BaseSensorOperator) 에 의해 데이터가 존재하지 않는 것을 확인했을 경우 index temaplte과 ilm template의 정보를 추가하여 index 생성 | index_name(str): 찾고자하는 sample 데이터 index 이름<br /> conn_id(str):‘connection’에 등록되어진 elasticsearch 연결 정보 |
| InsertOperator(BaseOperator) | './sample_data'에 적재되어진 데이터를 elasticsearch에 추가 | log_name(str): 찾고자하는 sample 데이터 index 이름<br > conn_id(str):‘connection’에 등록되어진 elasticsearch 연결 정보 |

</br>

## TASK
---

<img width="625" alt="image" src="https://github.com/cucuridas/operator_custom_tg/assets/65060314/0388f527-b2d3-4cb4-b174-3e810351fae4">

총 3개의 task를 가지고 있으며 각각의 task는 아래의 표를 참고

| task name | Using operator |
| --- | --- |
| check_sensor_task_{index_name} | CheckSensorOperator(BaseSensorOperator) |
| make_index_{index_name} | MakeIndexOperator(BaseOperator) |
| insert_sample_data_{index_name} | InsertOperator(BaseOperator) |