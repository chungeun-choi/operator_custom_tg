from typing import Any
from airflow.utils.context import Context
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import string
import pandas as pd
from airflow.models.variable import Variable
from airflow.models.baseoperator import BaseOperator

from dotenv import load_dotenv
import os


class config:
    DRIVER: str = os.getenv("DRIVER", "chrome")


class Crawler:
    def __init__(self, url):
        try:
            self._driver_name = Variable.get("crawler_driver", deserialize_json=True)
        except:
            self._driver_name = config.DRIVER

        self._url = url

    def _make_dirver(self):
        if self._driver_name.lower() == "chrome":
            self._driver = webdriver.Chrome(
                "/opt/airflow/add/chrome_driver/chromedriver"
            )

    def get_html(self):
        return self._driver.get(self._url)


class CollectingData(Crawler):
    pass


class CrawllingOperator(BaseOperator):
    def __init__(self, parsing_elements):
        super().__init__()
        self._crawler_obj = Crawler().get_html()
        self._parsing_elements = parsing_elements

    def execute(self, context: Context):
        self._crawler_obj.find_elements_by_css_selector(self._parsing_elements)
