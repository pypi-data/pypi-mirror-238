#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time :2023/2/13 
# @Author :wsli
# @File : client.py
# @Software: PyCharm
import threading
import time

import redis
import json
class Bruce_redis():
    def __init__(self,pool):
        self.POOL=pool
        self.redis_client=redis.Redis(connection_pool=pool)
    def get(self, key):
        """
        获取单个值
        :param key:
        :return:
        """
        value = self.redis_client.get(key)
        return value

    def mget(self, *args):
        """
        获取多个值
        :param args:
        :return:
        """
        value = self.redis_client.mget(*args)
        return value

    def set(self, key, value):
        """
        设置单个值
        :param key:
        :param value:
        :return:
        """
        value = self.redis_client.set(key, value)
        return value

    def mset(self, *args, **kwargs):
        """
        设置多个键值
        :return:
        """
        value = self.redis_client.mset(*args, **kwargs)
        return value

    def is_key_true(self, key):
        """
        判断key值是否存在
        :return:
        """
        status = self.redis_client.exists(key)
        return status

    def del_key(self, key):
        """
        删除key
        :param key:
        :return:
        """
        status = self.redis_client.delete(key)
        return status

    def clear_db_data(self):
        """
        清除当前数据库中所有数据
        :return:
        """
        pass

    def clear_dball_data(self):
        """
        清除所有库中所有数据
        :return:
        """
        pass

    def set_json(self, keyName, jsonstr):
        """
        存入json到redis中
        :return:
        """
        jsonstr = json.dumps(jsonstr)
        status=self.redis_client.set(keyName, jsonstr)
        return status

    def get_json(self, keyName):
        """
        获取key的json值
        :param keyName:
        :return:
        """

        val = self.get(keyName)
        return json.loads(val)





class Bruce_redis_pool:
    def __init__(self,host='localhost', port=6379, db=0, pool_size=10,password="",decode_responses=True):
        #创建连接池
        self.host = host
        self.port = port
        self.db = db
        self.pool_size = pool_size
        self.password=password
        self.decode_responses = decode_responses
        self.pool = self._create_pool()


    def _create_pool(self):
        return redis.BlockingConnectionPool(host=self.host, port=self.port, password=self.password, db=self.db, decode_responses=self.decode_responses,
                             max_connections=self.pool_size)



    def create_redis_client(self):
        """
        连接池中拿一个连接，自动回收连接
        """
        # 获取Redis连接
        conn = Bruce_redis(self.pool)
        return conn


class Redis_mock_error:
    def __init__(self):
        pass
    def mock_client_max(self,host='localhost', port=6379, db=0, max_connections=10000,password=""):
        """
        错误示范
        模拟redis客户端连接数超过10000
        cc=Redis_mock_error()
        cc.mock_client_max()
        """
        connections = []
        try:
            for _ in range(max_connections):
                print(f"Creating connection {len(connections) + 1}/{max_connections}")
                connection = redis.Redis(host=host, port=port, db=db,password=password)
                connection.set('key', 'value')  # Do some work with the connection
                connections.append(connection)
        except redis.exceptions.ConnectionError as eroor:
            print("redis连接数已经达到最大值,不能连接了",eroor)
        except Exception as e:
            print("e",e)




"""
redis-py官网https://redis.readthedocs.io/en/latest/examples.html
redis-py库提供了两种连接池：BlockingConnectionPool和ConnectionPool。它们的主要区别在于当连接池中没有可用连接时的行为不同。
BlockingConnectionPool会阻塞并等待直到有可用连接为止，而ConnectionPool则会立即引发ConnectionError异常。
因此，如果你的应用程序需要在没有可用连接时等待并重试，则应该使用BlockingConnectionPool。如果你的应用程序需要立即知道连接池中是否有可用连接，则应该使用ConnectionPool。
另外，BlockingConnectionPool还可以设置一个timeout参数，以避免无限期地等待可用连接。如果在指定的时间内没有可用连接，则会引发ConnectionError异常。
总之，如果你需要在没有可用连接时等待并重试，则使用BlockingConnectionPool；如果你需要立即知道连接池中是否有可用连接，则使用ConnectionPool
"""







