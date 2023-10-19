
### login 및 DAG desciprtion 보는 방법

- login

    ![logins](https://github.com/cucuridas/operator_custom_tg/assets/65060314/63cd8b87-fc0e-4e50-98d8-b763bea5502b)

- DAG desciption 보는 방법
    
    ![Jun-05-2023 17-25-13](https://github.com/cucuridas/operator_custom_tg/assets/65060314/8c87d151-abfd-4e8f-b78d-eb37c8904865)

<br>

## Airflow local 실행 방법

### 1) docker 설치(docker-compose 포함)

- Install Ubuntu

    [Docker Engine overview](https://docs.docker.com/engine/)

- Install Desktop on Mac

    [Install Docker Desktop on Mac](https://docs.docker.com/desktop/install/mac-install/)

</br> 

### 2) Elasticsearch container 생성

<span style="color:red"> './docker/dev/' 디렉토리에 관련 yaml파일이 존재합니다</sapn>

***해당 yaml 파일에는 kibana도 포함되어져 있습니다** 

elasticsearch : localhost:9200
kibana: localhost:5601

```c
docker-compose -f elasticsearch.yaml up -d
```

</br> 

### 3) Airflow container 생성
<span style="color:red"> './docker/dev/' 디렉토리에 관련 yaml파일이 존재합니다</sapn>

Airflow-webserver: localhost:8080

```c
docker-compose up -d
```

<img width="907" alt="image" src="https://github.com/cucuridas/operator_custom_tg/assets/65060314/92ecfa81-40c8-4563-b300-8216796bcae6">


<br>

## 참조 내용

[ ‘Data Pipelines with Apache Airflow’ 내용을 통해 커스텀 오퍼레이터 만들기](READBOOKS.md)

</br>
