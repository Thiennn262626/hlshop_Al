import os

from dotenv import load_dotenv
import json
import redis

load_dotenv()

class Redis:
    def __init__(self):
        self.r = redis.Redis(
            host=os.getenv("REDIS_HOST_NAME"),
            port=os.getenv("REDIS_PORT"),
            username=os.getenv("REDIS_USER_NAME"),
            password=os.getenv("REDIS_ACCESS_PASSWORD"),
        )
        print("Redis init.")

    def set_redis_data(self, key, value, expiration_time=None):
        self.r.set(key, json.dumps(value))
        # if expiration_time is not None:
        #     self.set_expiration_time(key, expiration_time)

    def get_redis_data(self, key):
        value = self.r.get(key)
        if value is None:
            return None
        return json.loads(self.r.get(key))

    def set_expiration_time(self, key, time):
        self.r.expire(key, time)

redis_instance = Redis()