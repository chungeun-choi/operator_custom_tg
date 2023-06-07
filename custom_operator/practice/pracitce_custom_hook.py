from airflow.hooks.base import BaseHook
from requests.sessions import Session

# 영화와 관련되어진 정보를 갱신하기위해 영화 데이터를 제공해주는 서버와 연결하는 서비스입니다
class MovielensHook(BaseHook):
    # connection 테이블에 연결될 서버의 정보가 없을 경우 기본 정보를 받아와 연결을 하기위해 초기화합니다
    DEFAULT_HOST = "movielens"
    DEFAULT_SCHEMA = "http"
    DEFAULT_PORT = 5000

    # 해당 클래스의 객체를 생성합니다 입력 받는 값은 conn_id를 통해서 연결 객체를 BaseHook을 통해 전달 받습니다
    def __init__(self, conn_id, context=None):
        super().__init__(context)
        self._conn_id = conn_id
        self._session = None
        self._base_url = None

    # get_connection 함수를 통해 conn_id와 매칭되는 연결정보를 가져옵니다
    def get_conn(self) -> Session:
        if self._session is None:  # -> 단일 책임의 원칙에 따라 해당 내용은 분리되어야할듯...
            config = self.get_connection(self._conn_id)
            schema = config.schema or self.DEFAULT_SCHEMA
            host = config.host or self.DEFAULT_HOST
            port = config.port or self.DEFAULT_PORT

            self.base_url = f"{schema}//{host}:{port}"

            self.session = Session()

        if config.login:
            self.session.auth = (config.login, config.password)

        return self.session, self.base_url

    # 조회되는 데이터의 양이 많을 경우 페이징을 통해 데이터를 나누는 작업을 진행하도록 합니다
    def _get_with_paginations(self, endpoint, params, batch_size=100):
        session, base_url = self.get_conn()

        offset = 0
        total = None
        while total is None or offset < total:
            response = session.get(
                base_url, params={**params, **{"offset": offset, "limit": batch_size}}
            )
            response.raise_for_status()
            response_json = response.json()

            yield from response_json["result"]

            offset += batch_size
            total = response_json["total"]

    # 페이징된 정보를 해당 함수를 통해서 호출하여 증분하여 호출합니다
    def get_ratings(self, start_date=None, end_date=None, batch_size=100):
        yield from self._get_with_paginations(
            endpoint="/ratings",
            params={"start_date": start_date, "end_date": end_date},
            batch_size=batch_size,
        )
