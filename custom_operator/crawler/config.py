from dotenv import load_dotenv
import os

class config:
    DRIVER: str = os.getenv("DRIVER","chrome")
    ELASTIC_PORT: int = os.getenv("SERVER_PORT",9200)
    SET_SSL :  bool = os.getenv("SET_SSL",False)
    SAMPLE_DATA : str = os.getenv("SAMPLE_DATA")
