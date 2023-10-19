# Operator_custom_tg

This repository contains a project that focuses on developing workflows for handling data in a data warehouse, specifically Elasticsearch. 

For information on setting up the environment, you can refer to this [링크](ENV_README.md).

## Software Architecture


The following diagram illustrates the software architecture in a production environment.

![image](https://github.com/cucuridas/operator_custom_tg/assets/65060314/6434016a-0f45-446d-827f-26159b8d270d)

## Workflows

The following descriptions visualize the roles and tasks of each workflow, explaining the process of handling data.

### Generator

This workflow is responsible for generating sample logs. It generates sample logs for data handling by defining specific times and log quantities in `Variables`. [Source Code Link](https://github.com/cucuridas/operator_custom_tg/tree/main/custom_operator/generator)

- Workflow: It stores sample log examples in the data warehouse (Elasticsearch).

    ![image](https://github.com/cucuridas/operator_custom_tg/assets/65060314/b8a8642a-7a71-443e-9aaf-520d262460fe)
    
- Workflow: It generates sample logs using log templates stored in the Redis cache.

    ![image](https://github.com/cucuridas/operator_custom_tg/assets/65060314/7d83c49c-3b14-4ae3-b22a-e20c70e9e8de)

### Datamart

This workflow is designed to create new data using the data stored in the data warehouse (Elasticsearch). By defining a query in the `Variable`, it generates and provides new data marts. [Source Code Link](https://github.com/cucuridas/operator_custom_tg/tree/main/custom_operator/datamart)

![image](https://github.com/cucuridas/operator_custom_tg/assets/65060314/668042c4-f740-4c09-91c4-d869e0e780cb)

### Detector

This workflow detects specific values as per user input in the data warehouse (Elasticsearch).

![image](https://github.com/cucuridas/operator_custom_tg/assets/65060314/c475b447-863f-4b94-a507-b9c06a8832e6)