import os

from api.ingestion_api.config import settings


class Config(object):
    def __init__(self, env: os._Environ):
        self.env = env

    @property
    def stream_name(self) -> str:
        return self.env.get("INGESTION_STREAM_NAME", settings.INGESTION_STREAM_NAME)

    @property
    def stream_host(self) -> str:
        return self.env.get("KINESIS_HOST", settings.KINESIS_HOST)


config = Config(os.environ)
