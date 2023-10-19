# Operator_custom_tg

이 저장소에는 데이터 웨어하우스, 특히 Elasticsearch를 사용한 데이터 처리 워크플로우를 개발하는 프로젝트가 포함되어 있습니다.

환경 설정에 관한 정보는 [링크](ENV_README.md)에서 확인하실 수 있습니다.

## 소프트웨어 아키텍처

---

다음 다이어그램은 프로덕션 환경에서의 소프트웨어 아키텍처를 보여줍니다.

![이미지](https://github.com/cucuridas/operator_custom_tg/assets/65060314/6434016a-0f45-446d-827f-26159b8d270d)

## 워크플로우

---

다음 설명은 데이터 처리 과정을 설명하며 각 워크플로의 역할과 작업을 시각화합니다.

### Generator

이 워크플로는 샘플 로그를 생성하는 역할을 합니다. `Variables`에서 특정 시간과 로그 양을 정의하여 데이터 처리를 위한 샘플 로그를 생성합니다. [소스 코드 링크](https://github.com/cucuridas/operator_custom_tg/tree/main/custom_operator/generator)

- 워크플로: 데이터 웨어하우스(Elasticsearch)에 샘플 로그 예시를 저장합니다.

    ![이미지](https://github.com/cucuridas/operator_custom_tg/assets/65060314/b8a8642a-7a71-443e-9aaf-520d262460fe)
    
- 워크플로: Redis 캐시에 저장된 로그 템플릿을 사용하여 샘플 로그를 생성합니다.

    ![이미지](https://github.com/cucuridas/operator_custom_tg/assets/65060314/7d83c49c-3b14-4ae3-b22a-e20c70e9e8de)

### Datamart

이 워크플로는 데이터 웨어하우스(Elasticsearch)에 저장된 데이터를 사용하여 새로운 데이터를 생성하는 데 사용됩니다. `Variable`에서 쿼리를 정의함으로써 새로운 데이터 마트를 생성하고 제공합니다. [소스 코드 링크](https://github.com/cucuridas/operator_custom_tg/tree/main/custom_operator/datamart)

![이미지](https://github.com/cucuridas/operator_custom_tg/assets/65060314/668042c4-f740-4c09-91c4-d869e0e780cb)

### Detector

이 워크플로는 데이터 웨어하우스(Elasticsearch)에서 사용자 입력에 따라 특정 값을 탐지하는 데 사용됩니다.

![이미지](https://github.com/cucuridas/operator_custom_tg/assets/65060314/c475b447-863f-4b94-a507-b9c06a8832e6)
