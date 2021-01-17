import pickle
from flask import g


class Cache:
    def __init__(self, key_prefix=None, timeout=300):
        self.key_prefix = key_prefix
        self.default_timeout = timeout

    def __contains__(self, key):
        return self._make_key(key) in g.redis_client

    def get(self, key, default=None):
        value = g.redis_client.get(self._make_key(key))
        if value is None:
            return default
        
        try:
            return pickle.loads(value)
        except pickle.UnpicklingError:
            return value

    def set(self, key, value, timeout=None):
        timeout = timeout or self.default_timeout
        value = pickle.dumps(value)
        return g.redis_client.set(self._make_key(key), value, ex=timeout)

    def delete(self, key):
        return g.redis_client.delete(self._make_key(key)) == 1

    def touch(self, key, timeout=None):
        timeout = timeout or self.default_timeout
        return g.redis_client.expire(self._make_key(key), timeout)

    def _make_key(self, key):
        if 
        if self.key_prefix:
            return '{}:{}'.format(self.key_prefix, key)
        return key