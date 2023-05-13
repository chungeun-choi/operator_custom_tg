import os
from dotenv import load_dotenv


load_dotenv()


class ElasticConfig:
    ELASTIC_HOST: str = os.getenv("SERVER_HOST","localhost")
    ELASTIC_PORT: int = os.getenv("SERVER_PORT",9200)
    SET_SSL :  bool = os.getenv("SET_SSL",False)
    SAMPLE_DATA : str = os.getenv("SAMPLE_DATA")
