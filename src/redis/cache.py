import logging

import redis
from src.config import redis_config


class CacheRedis:
    def __init__(self):
        self.host = redis_config.get('host')
        self.port = redis_config.get('port')
        self.db = redis_config.get('db')
        self.redis_db = redis.StrictRedis(host=self.host,
                                          port=self.port,
                                          db=self.db)

    def get_response_from_cache(self, message):
        try:
            response = self.redis_db.get(message).decode('utf-8')
            if response:
                return response
            else:
                return None
        except Exception as e:
            logging.getLogger().info(f'[ERROR] Fail to get cache response {str(e)}')
            return None

    def save_to_cache(self, message, response):
        # lưu message, response
        self.redis_db.set(message, response)
