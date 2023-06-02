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



# DAG -  Detect_data_by_using_userInput

## 내용
---

해당 DAG는 Elasticsearch에 적재되어진 데이터에서 사용자가 지정한 특정한 값이 발견되었을 때 사용자 지정 행위를 할 수 있도록 정의한 DAG입니다 

`DetectSensorOperator` operator를 특정 기준으로 데이터를 탐지하게됩니다

사용자 지정 기준으로는 `frequency(탐지 빈도)`, `interval(탐지되는 시간범위)` 두가지를 입력받아 설정되어지게 됩니다

## 사용법
---

### 1) Variable 값 정의

<img width="742" alt="detec_varables" src="https://github.com/cucuridas/operator_custom_tg/assets/65060314/9f580857-b794-40ab-8da0-20c0e6bff277">

```c
1. 상단의 메뉴바에서 'Admin' 클릭
2. 'Admin' 하위 메뉴에서 'Variables' 클릭
3. '+' 버튼을 눌러 'detec_rule' 새롭게 생성, 'detec_rule'가 생성되어져 있을 경우 수정 버튼을 눌러 변경
4. key, value를 통해 데이터 정의 *key의 이름은 'detec_rule' 고정
```

### 3) Operator 객체 생성하여 파라미터 정의

- **각 operator 파라미터 내용 (BaseOperator 내용은 생략되어 있습니다)**

| Operator name | description | parameter description |
| --- | --- | --- |
| DetectSensorOperator(BaseSensorOperator) | ‘Variables’의 key ‘detec_rule’ 의 값을 받아와 사용자 설정에 의한 탐지를 진행합니다 | input(UserDetecInput): dag에서 사용하게 될 사용자의 입력 객체를 전달 받습니다 <br /> conn_id(str):‘connection’에 등록되어진 elasticsearch 연결 정보 |
| EmailOperator(BaseOpeartor) | Airflow에서 제공하는 operator 중 하나로서 사용자에 등록되어진 email 정보로 메일을 발송합니다 | Airflow 공식 doc 참조 |
- **Variables 데이터 형태 (json) - UserDetectInput(class)**
    
    Variables의 키 ‘detect_rule’에 정의되어진 값은 UserDetectInput 클래스를 통해 객체로 변환 되어져 사용됩니다 아래의 표는 UserDetectInput 클래스의 속성 값에 대한 설명입니다
    
    | class.attribute | description | type |
    | --- | --- | --- |
    | _detection_target | 탐지하게되는 대상입니다, 입력받는 형태는 dictionary 형태로 ‘{index field name}:{value}’ 입니다 | dict |
    | _frequency | 탐지되는 빈도를 나타냅니다 _interval 기간안에 해당 값 만큼 탐지되었을 때 True를 반환하도록 합니다 | int |
    | _interval | 탐지되는 시간 범위를 나타냅니다 | int |

</br>

## TASK
---

내용 추가 필요