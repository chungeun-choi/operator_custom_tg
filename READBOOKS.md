# ‘Data Pipelines with Apache Airflow’ 내용을 통해 커스텀 오퍼레이터 만들기

# 패키지 개발 과정

1. Custom Hook 개발
2. Custom Operator 개발
3. Custom sensor 개발
4. 패키징

# Custom Hook 개발

Custom Hook 개발은 Airflow에서 모든 훅의 추상 클래스의 ‘BaseHook’ 클래스의 서브클래스로 생성하며 Airflow metastore(Connections) 테이블을 통해 사용자가 정의한 connection information을 통해 Connection 객체를 구현하는 것을 권장합니다

### BaseHook 클래스

- 다이어그램
    
    ![https://user-images.githubusercontent.com/65060314/233025262-e63b058a-5357-4145-b135-a961ddff2da7.png](https://user-images.githubusercontent.com/65060314/233025262-e63b058a-5357-4145-b135-a961ddff2da7.png)
    

- **Class 상세 설명**
    
    Airflow 공식 doc : 
    
    [airflow.hooks.base — Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/hooks/base/index.html)
    
    | 함수 이름 | 메소드 타입 | 내용 |
    | --- | --- | --- |
    | get_connections | classmethod | connection_id 를 통해서 연결관련 정보를 iterable한 자료형으로 모두 불러옵니다 |
    | get_connection | classmethod | connection_id 연결 정보를 단일로 조회합니다 |
    | get_hook | classmethod | 해당 connection id를 위한 기본 hook을 전달합니다 |
    | get_conn | abstract | 구현해야하는 함수로서 연결에 대한 객체를 리턴하는 함수입니다 |
    

### [예제] MovielensHook

영화 정보를 전달해주는 서버와 connection을 연결하여 영화 순위 기능 제공 받기

[소스코드 링크](/custom_operator/practice/pracitce_custom_hook.py)

# 커스텀 오퍼레이터 개발

### BaseOperator 클래스

- **Class 상세 설명**
    
    Airflow 공식 doc: 
    
    [airflow.models.baseoperator — Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/baseoperator/index.html)
    
    **Class parameter**
    
    | 파라미터 명 | 입력 타입 | 내용 |
    | --- | --- | --- |
    | task_id | str | task를 위한 유일한 아이디 |
    | owner | str | task의 onwer를 정의  |
    | email_on_retry | bool | task가 재시작 되었을 때 이메일 알람을 받을 것인지에 대한 내용 |
    | email_on_failure | bool | task가 실패하였을 때 이메일 알람을 받을 것인가 |
    | retries | int | task가 실패 했을 경우 재시도하는 횟수를 지정 |
    | retry_delay | timedelta, float | task 재시도 간 시간 간격을 지정 |
    | retry_exponentioal_backoff | bool | 해당 값을 true로 함으로써 재시도 간격을 backoff 알고리즘을 통해 점진적으로 늘릴 수 있음 |
    | max_retry_delay | timedelta, float, None | 재시도 간격간 지연시간의 한계를 지정 |
    | start_date | datetime, None | task를 위한 시작 날짜를 지정, 해당 값을 통해 처음 실행되는 task 객체의 execution_date를 지정, 선행 task에 대해 종속성이 존재할 경우 주의가 필요한 설정 |
    | end_date | datetime, None | schedule이 씉나는 시점의 날짜 |
    | depends_on_past | bool | true로 설정 시 task 객체는 이전 객체가 성공하거나 스킵되었을 시에만 순서대로 진행되게 끔 설정 |
    | wait_fro_downstream | bool | true로 설정 시, 특정 task의 객체는 이전 task의 다운스트림 아래에 있는 task가 완료 될때까지 기다리게 끔 설정 |
    | dag | DAG | 해당 task가 포함된 dat 객체 |
    | priority_weigh | int | task의 중요도를 설정,executor에 의해서 트리거 될때 해당 값이 높게 설정되어진 항목을 먼저 백업 |
    | weight_rule | str | weighting 함수는 task의 전체 가중치를 효과적으로 반영하기 위해 사용, option의 값으로는 downstream, upstream, absolute 등이 존재
    downstream:  다운스트림으로 설정된 경우 작업의 유효 가중치는 모든 다운스트림 하위 항목의 총합
    upstream: 업스트림으로 설정된 경우 유효 가중치는 모든 업스트림 상위 항목의 합계
    absolute: 지정한 priority_weight 값을 통해 설정됨 |
    | queue | str | 어떠한 queue에서 job을 실행 시킬 지 설정합니다. Airflow worker를 실행시킬때 정의한 celery worker의 queue 이름 |
    | pool | str, None | pools 페이지에서 설정한 pool을 사용 |
    | pool_slots | int | 사용할 pool slot을 지정합니다, 해당 pool slot에서 가용가능한 task 갯수만큼만 실행 |
    | sla | timedelta,None | 특정 시간을 지정해둠으로 써 해당 task에 대한 요구사항을 지정합니다 해당 시간이 지날 경우 SLA misses에 기록하거나 이메일을 전송 |
    | execution_timeout | timedelta,None | 해당 task가 실행 되기까지의 timeout 시간을 설정 |
    | on_failure_callback | TaskStateChangeCallback, None | 해당 task가 실패 했을 때 실행 시킬 함수를 정의 |
    | on_execute_callback | TaskStateChangeCallback,None | task가 정상적으로 실행되기 전 호출할 함수를 정의 |
    | on_success_callback | TaskPreExecuteHook | task가 성공적으로 완료되었을 때 호출할 함수를 정의 |
    | pre_execute | TaskPreExecuteHook,None | task가 실행되기전 실행할 함수를 정의 |
    | post_execute | TaskPostExecuteHook | task가 정상적으로 실행 된 뒤 실행 시킬 함수를 정의 |
    | trigger_rule | str | 현재 트리거를 트리거하기 위해 선행 작업의 의존성에 대한 정책을 정의
    [ex] all_success : 선행 작업들이 모두 성공해야 현재 작업을 실행 |
    | resources | dic[str,any], None | resource 매개변수의 이름 |
    | run_as_user | str,None | unix의 어떤 user의 권한으로 해당 task를 실행 시킬 것인지 정의 |
    | max_active_tis_per_dag | int, None | 해당 task가 소속된 dag 내에서 동시에 실행시킬 수 있는 갯수를 제한 |
    | executor_config | dict,None | 특정 executor가 추가적인 매개변수를 필요로 할 때 사용 |
    | do_xcom_push | bool | 해당 값이 true 일경우 task(operator)의 결과 값을 xcom 테이블에 저장 |
    | task_group | TaskGroup | task가 속해진 task group을 정의 |
    | doc | str,None | 해당 task에 대한 documentation을 정의, 정의되어진 내용은 webserver를 통해 출력 |
    | doc_md | str,None | doc 과 동일 md 형태의 string 데이터를 입력 받아 변환 |
    | doc_rst | str,None | doc 과 동일 rst 데이터를 입력 받아 변환 |
    | doc_json | str,None | doc 과 동일 json 데이터를 입력 받아 변환 |
    | doc_yaml | str,None | doc 과 동일 yaml 데이터를 입력 받아 변환 |
    

## [예제] MovielensFetchRatingsOperator

MovielenHook 을 통해 구현되어진 get_ratings를 호출하여 데이터를 가져오고 해당 데이터를 저장하는 operator

[소스코드 링크](/custom_operator/practice/pracitce_custom_operator.py)

# 커스텀 센서 개발

## BaseSeonsorOperator 클래스

- **Class 상세 설명**
    
    Airflow 공식 document : 
    
    [airflow.sensors.base — Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/sensors/base/index.html)
    
    **parmeter**
    
    | 이름 | 타입 | 내용 |
    | --- | --- | --- |
    | sofft_fail | bool | true로 설정하여 실패 시 작업을 건너뛰기로 표시 |
    | poke_interval | float | poke 함수를 통해 확인 시 각 확인작업에 대한 시간 간격 |
    | timeout | float | 해당 작업이 완료되기까지의 시간 |
    | mode | str | 어떤 방식으로 sensor를 작동 시킬 것인지에 대한 설정 (poke: 설정 시 worker 슬롯을 점유, reschedule: worker 슬롯을 점유하지 않고 탐지 시 실행) |
    | exponetial_backoff | bool | 센서로 탐지하는 간격을 back off 알고리즘을 통해 점진적으로 늘리는 설정 |
    | max_wait | timedelta,float,None | 센서로 탐지하는 간격 간의 max 시간을 초기화 |
    
    **fucntion**
    
    | 이름 | 내용 |
    | --- | --- |
    | poke(context) | 해당 클래스를 상속받는 클래스는 이 함수를 재정의 해야함 |
    | execute(context) | operator를 실행하기 위한 메인 함수 |
    

## [예제] MovielensRatingsSensor

사용자에 의해 입력받은 특정 기간동안 평점 데이터가 존재하는 지 여부를 확인하여 True, False를 리턴하는 sensor operator

[소스코드 링크](/custom_operator/practice/paractice_custom_sensor.py)