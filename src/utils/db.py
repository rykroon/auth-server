import os
from mongoengine import connect
import redis

mongo_db = os.getenv('MONGO_DB')
mongo_host = os.getenv('MONGO_HOST', 'localhost')
mongo_port = os.getenv('MONGO_PORT', 27017)
connect(mongo_db, host=mongo_host, port=mongo_port)

redis_host = os.getenv('REDIS_HOST')
redis_pass = os.getenv('REDIS_PASSWORD')
redis_connection_pool = redis.ConnectionPool(host=redis_host, password=redis_pass, db=0)

def get_redis_client():
    return redis.Redis(connection_pool=redis_connection_pool)