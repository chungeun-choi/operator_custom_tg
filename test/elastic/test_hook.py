import sys
sys.path.append("/Users/cucuridas/Desktop/operator_custom_tg")

from custom_operator.elastic.hook import ElasticsearchHook



def test_connection():
    test_obj = ElasticsearchHook("test")
    test_obj.ping()

if __name__ == "__main__":
    pass