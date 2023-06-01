from collections import Counter
import sys
sys.path.append("/Users/cucuridas/Desktop/operator_custom_tg")
sys.path.append("/opt/airflow/dags")

from datamart.datamart import *
from datetime import datetime


TEST_OBJ = UserInput(
    index_name="waf",
    query_type="sql",
    query="SELECT * FROM waf",
    datamart_name="test_obj_sql_1",
    save_type="warehouse"
)

TEST_OBJ2 = UserInput(
    index_name="waf",
    query_type="dsl",
    query={
  "sort": [
    {
      "@timestamp": {
        "order": "desc"
      }
    }
  ]
},
    datamart_name="test_obj_sql_1",
    save_type="warehouse"
)


def test_MakeDataMartOperator():
    input= {
        "input": TEST_OBJ,
        "conn_id":"docker_elastic"
    }

    input2 ={
        "input" : TEST_OBJ2,
        "conn_id":"docker_elastic"
    }
    
    obj = MakeDataMartOperator(**input)
    obj.execute(context=None)
    # value = obj.get_data()
    # print("test")

    # convert = obj._convert_dataframe(value)
    # print(convert)

    # obj2 =  MakeDataMartOperator(**input2)
    # value2= obj2.get_data()

    # convert = obj2._convert_dataframe(value2)
    # print(convert)
    pass




if __name__ == "__main__":
    test_MakeDataMartOperator()
    pass