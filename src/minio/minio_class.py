from minio import Minio
from src.config import minio_config, WEBHOOK_URL
class MinIO():
    def __init__(self):
        self.access_key = minio_config.get('access_key')
        self.secret_key = minio_config.get('secret_key')

    def connect(self):
        minio_client = Minio(WEBHOOK_URL, access_key=self.access_key, secret_key=self.secret_key, secure=False)
        return minio_client
    