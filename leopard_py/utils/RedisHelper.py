import pickle

import redis

import Constants as constants


class RedisHandler:
    def __init__(self):
        # 创建连接池
        self.pool = redis.ConnectionPool(host=constants.EDIT_REDIS_HOST, port=constants.EDIT_REDIS_PORT,
                                         db=constants.EDIT_REDIS_DB)
        # 创建链接
        self.conn = redis.Redis(connection_pool=self.pool)

    # 存放字符串
    def set_str(self, key, value, time=0):
        if time == 0:
            self.conn.setex(key, value)
        else:
            self.conn.setex(key, time, value)

    # 存放字符串
    def set_str_pickle(self, key, value, time=0):
        value = pickle.dumps(value)
        if time == 0:
            self.conn.setex(key, value)
        else:
            self.conn.setex(key, time, value)

    # 获取字符串
    def get_str(self, key):
        value = self.conn.get(key)
        if value:
            value = str(value, encoding='utf8')
        else:
            return ""
        return value

    def get_str_pickle(self, key):
        value = self.conn.get(key)
        if value:
            return pickle.loads(self.conn.get(key))
        else:
            return None
        return pickle.loads(self.conn.get(key))

    # 删除字符串
    def del_str(self, key):
        return self.conn.delete(key)

    def insert_set(self, key, value):
        # for i in value:
        self.conn.sadd(key, value)

    def find_set(self, key):
        value = self.conn.smembers(key)
        if value:
            list = []
            for i in value:
                list.append(str(i, encoding='utf8'))
            return list
        else:
            return None

    def insert_hash(self, key, params, value):
        self.conn.hset(key, params, value)

    def insert_hash_mapping(self, key, name, mapping):
        self.conn.hset(key, name, mapping)

    def get_hash_mapping(self, key, name):
        return json.loads(self.conn.hget(key, name))

    def get_value(self, key, params):
        return self.conn.hget(key, params)

    def get_all_value(self, key):
        return self.conn.hgetall(key)

    def del_hash(self, key, params):
        self.conn.hdel(key, params)

    def list_push(self, key, val):
        self.conn.lpush(key, val)

    def list_pop(self, key):
        return self.conn.rpop(key)

    def list_len(self, key):
        if self.conn.exists(key):
            return self.conn.llen(key)
        else:
            return 0


getConnect = RedisHandler()
