from collections import Counter
import sys

sys.path.append("/Users/cucuridas/Desktop/operator_custom_tg")
sys.path.append("/opt/airflow/dags")

from crawler.crawler import *


def test_Crawler():
    test_obj = Crawler("https://www.musinsa.com/app/")
    test_obj._make_dirver()

    print(test_obj.get_html())


if __name__ == "__main__":
    test_Crawler()
