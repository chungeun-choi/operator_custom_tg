from airflow.www.utils import UIAlert
from markupsafe import Markup

DASHBOARD_UIALERTS = [
    #UIAlert('<h4>Grafana 대시보드 주소입니다<h4> \n 링크 -  <a href="http://grafana.cucuridas.info:3000/d/b90ff124-63fa-4e97-988f-cfef4921a287/home?orgId=1">grafana - dashboard</a> </br> 접속 계정 - ID: test, PW: test1231!' , html=True),
    #UIAlert('<h4>Topology 정보입니다<h4>  <img src="https://user-images.githubusercontent.com/65060314/243423544-86ecfc8f-a935-4741-ac6a-0b959536acbc.png" alt="My Image">' , html=True),
    UIAlert(Markup('<h4>Topology 정보<h4>  <img src="https://user-images.githubusercontent.com/65060314/243426199-c476b33b-7742-4f73-970a-d0512458ee3c.png" alt="My Image">'))
]