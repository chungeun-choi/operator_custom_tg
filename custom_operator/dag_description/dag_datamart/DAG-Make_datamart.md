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


# DAG -  Make_datamart

## 내용
----

해당 DAG는 Elasticsearch에 적재되어진 Index를 통해 사용자의 목적에 맞는 데이터 마트를 생성하기위한 DAG입니다 SQL query와 DSL query를 지원합니다

key `save_type` 의 value 값을 통해 저장 방식을 지원합니다 현재 저장방식은 ‘csv’와 , ‘warehouse(저장소 현재는 elasticsearch)’입니다

</br>

## 사용법
---

### 1) Variable 값 정의

<img width="845" alt="image" src="https://github.com/cucuridas/operator_custom_tg/assets/65060314/e1440336-271c-4d0f-a804-0b2fa8590ee3">

```c
1. 상단의 메뉴바에서 'Admin' 클릭
2. 'Admin' 하위 메뉴에서 'Variables' 클릭
3. '+' 버튼을 눌러 'datamart_list' 새롭게 생성, 'datamart_list'가 생성되어져 있을 경우 수정 버튼을 눌러 변경
4. key, value를 통해 데이터 정의 *key의 이름은 'datamart_list' 고정
```

### 2) Operator 객체 생성하여 파라미터 정의

- 각 operator 파라미터 내용 (BaseOperator 내용은 생략되어 있습니다)

| Operator name | description | parameter description |
| --- | --- | --- |
| MakeDataMartOperator(BaseOperator) | ‘Variables’의 key ‘datamart_list’ 의 값을 받아와 데이터 마트를 생성합니다 | input(UserInput): datamart에서 사용하게 될 사용자의 입력 객체를 전달 받습니다 <br /> conn_id(str):‘connection’에 등록되어진 elasticsearch 연결 정보 |

- **Variables 데이터 형태 (json) - UserInput(class)**

| class.attribute | description | type |
| --- | --- | --- |
| index_name | 데이터 마트를 만들고자하는 index의 이름을 입력받습니다 | str |
| query_type | 조회시 사용하 query의 타입을 입력합니다 (sql or dsl) | str(sql or dsl) |
| query | 조회 시 사용하게될 query를 입력 받습니다 query_type이 sql 일 경우 str타입을, dsl일 경우 dict 타입의 데이터를 입력받습니다 | dict,str |
| datamart_name | 새로 생성하게되는 data mart의 이름을지정합니다 | str |
| save_type | 저장하고자하는 타입을 입력합니다 (현재 csv와 data warehouse 두가지 방식을 지원합니다) | str (csv or warehouse) |

<br/>

## TASK
---

<img width="346" alt="image" src="https://github.com/cucuridas/operator_custom_tg/assets/65060314/98475698-0344-4a9d-9cc2-a196d5cee47f">

총 1개의 task를 가지고 있으며 task는 아래의 표를 참고

| task name | Using operator |
| --- | --- |
| make_data_task_{data mart rule name} | MakeDataMartOperator(BaseOperator) |