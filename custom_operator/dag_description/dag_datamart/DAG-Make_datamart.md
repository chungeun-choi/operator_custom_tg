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

해당 DAG는 Elasticsearch에 적재되어진 Index를 통해 사용자의 목적에 맞는 데이터 마트를 생성하기위한 DAG입니다 SQL query와 DSL query를 지원합니다

key `save_type` 의 value 값을 통해 저장 방식을 지원합니다 현재 저장방식은 ‘csv’와 , ‘warehouse(저장소 현재는 elasticsearch)’입니다

## 사용법

### 1) DAG trigger를 통해 실행

![trigger_on](https://github.com/cucuridas/operator_custom_tg/assets/65060314/586f6c5c-ad49-41bf-b1af-8db10982818f)

![trigger_input](https://github.com/cucuridas/operator_custom_tg/assets/65060314/a27e7dea-eaaa-4404-8ab4-b76ae4a7844f)

![input_value](https://github.com/cucuridas/operator_custom_tg/assets/65060314/23164263-ded4-4c2e-8550-f8c80b884983)

![trigger_button](https://github.com/cucuridas/operator_custom_tg/assets/65060314/4d98ef7f-bc26-4275-ada1-032f229c5099)

### 3) 파라미터 값 내용

| class.attribute | description | type |
| --- | --- | --- |
| index_name | 데이터 마트를 만들고자하는 index의 이름을 입력받습니다 | str |
| query_type | 조회시 사용하 query의 타입을 입력합니다 (sql or dsl) | str(sql or dsl) |
| query | 조회 시 사용하게될 query를 입력 받습니다 query_type이 sql 일 경우 str타입을, dsl일 경우 dict 타입의 데이터를 입력받습니다 | dict,str |
| datamart_name | 새로 생성하게되는 data mart의 이름을지정합니다 | str |
| save_type | 저장하고자하는 타입을 입력합니다 (현재 csv와 data warehouse 두가지 방식을 지원합니다) | str (csv or warehouse) |
| email | save_type 의 값이 csv일 경우 만들어진 csv 파일을 해당 값으로 정의되어진 email 주소로 전달되게 됩니다 | str |

## TASK

![task_data_mart](https://github.com/cucuridas/operator_custom_tg/assets/65060314/12ae896c-1ae2-4c61-8b14-c92e8e331e65)

총 6개의 task를 가지고 있으며 task는 아래의 표를 참고

| task name | Using operator | desciption |
| --- | --- | --- |
| make_data_mart_task | MakeDataMartOperator(BaseOperator) | Elasticsearch에 API를 호출하여 결과를 조회해온 뒤 데이터 프레임으로 변환합니다 |
| check_save_type | BranchPythonOperator | 입력받은 params의 값을 통해 저장 타입을 확인합니다 (현재 csv와 warehouse를 지원합니다) |
| make_csv_file | PythonOperator | params[”save_type”]이 ‘csv’ 일 경우 실행 되며 만들어진 데이터 프레임을 csv 형태로 저장합니다 |
| save_elasticsearch | SaveElasticsearchOperator(BaseOperator) | params[”save_type”]이 ‘warehouse’ 일 경우 실행 되며 만들어진 데이터 프레임을 csv 형태로 저장합니다 |
| send_email_with_datamart_csv | EmailOperator | 만들어진 csv 파일을 params[”email”] 값으로 전송합니다 |
| delete_csv_file | PythonOperator | 기존의 만들어진 csv 파일을 삭제합니다 |