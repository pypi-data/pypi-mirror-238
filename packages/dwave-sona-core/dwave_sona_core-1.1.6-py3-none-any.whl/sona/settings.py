import os
from typing import Dict, List, Optional

from pydantic import RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SONA_INFERENCER_CLASS: Optional[str] = None

    # Core Storage settings
    SONA_STORAGE_LOCAL_PATH: str = os.getcwd()
    SONA_STORAGE_S3_SETTING: Dict = dict()
    SONA_STORAGE_S3_BUCKET: str = "sona"
    SONA_SOURCE_GOOGLE_SERVICE_ACCOUNT_INFO: Optional[Dict] = None

    # Worker base settings
    SONA_WORKER_CLASS: str = "sona.worker.workers.InferencerWorker"
    SONA_WORKER_TOPIC_PREFIX: str = "sona.inferencer."

    # Worker consumer settings
    SONA_WORKER_CONSUMER_SQS_SETTING: Optional[Dict] = None
    SONA_WORKER_CONSUMER_KAFKA_SETTING: Optional[Dict] = None
    SONA_WORKER_CONSUMER_REDIS_URL: Optional[RedisDsn] = None
    SONA_WORKER_CONSUMER_REDIS_GROUP: Optional[str] = "sona.anonymous"

    # Worker producer settings
    SONA_WORKER_PRODUCER_SQS_SETTING: Optional[Dict] = None
    SONA_WORKER_PRODUCER_KAFKA_SETTING: Optional[Dict] = None
    SONA_WORKER_PRODUCER_REDIS_URL: Optional[RedisDsn] = None

    # Middleware settings
    SONA_MIDDLEWARE_CLASSES: List[str] = []
    SONA_MIDDLEWARE_SUPERVISOR_SQS_SETTING: Optional[Dict] = None
    SONA_MIDDLEWARE_SUPERVISOR_KAFKA_SETTING: Optional[Dict] = None
    SONA_MIDDLEWARE_TRACER_SERVICE_NAME: str = 'SONA API'
    SONA_MIDDLEWARE_TRACER_JAEGER_HOST: str = 'localhost'
    SONA_MIDDLEWARE_TRACER_JAEGER_PORT: int = 6831

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
