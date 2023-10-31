# encoding: utf-8
import time

import pymysql
from dbutils.pooled_db import PooledDB

class Bruce_mysql():
    # 初始化
    def __init__(self,dbName, host="localhost",port=3306, user="root", passwd="123456"):
        self.host = host
        self.port=port
        self.user = user
        self.passwd = passwd
        self.dbName = dbName
        self.connet()

    # 连接数据库，需要传数据库地址、用户名、密码、数据库名称，默认设置了编码信息
    def connet(self):
        try:
            self.db = pymysql.connect(host=self.host,
                                      port=self.port,
                                      user=self.user,
                                      password=self.passwd,
                                      db=self.dbName,
                                      use_unicode=True,
                                      charset='utf8')
            self.cursor = self.db.cursor()
        except Exception as e:
            return e

    # 关闭数据库连接
    def close(self):
        try:
            self.cursor.close()
            self.db.close()
        except Exception as e:
            return e

    # 查询操作，查询单条数据
    def get_one(self, sql):
        # res = None
        try:
            self.connet()
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            self.close()
        except Exception:
            res = None
        return res

    # 查询操作，查询多条数据
    def get_all(self, sql):
        # res = ()
        try:
            self.connet()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.close()
        except Exception:
            res = ()
        return res

    # 查询数据库对象
    def get_all_obj(self, sql, tableName, *args):
        resList = []
        fieldsList = []
        try:
            if (len(args) > 0):
                for item in args:
                    fieldsList.append(item)
            else:
                fieldsSql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s' and table_schema = '%s'" % (
                    tableName, self.dbName)
                fields = self.get_all(fieldsSql)
                for item in fields:
                    fieldsList.append(item[0])

            # 执行查询数据sql
            res = self.get_all(sql)
            for item in res:
                obj = {}
                count = 0
                for x in item:
                    obj[fieldsList[count]] = x
                    count += 1
                resList.append(obj)
            return resList
        except Exception as e:
            return e

    # 数据库插入、更新、删除操作
    def insert(self, sql):
        return self.__edit(sql)

    def update(self, sql):
        return self.__edit(sql)

    def delete(self, sql):
        return self.__edit(sql)

    def __edit(self, sql):
        # count = 0
        try:
            self.connet()
            count = self.cursor.execute(sql)
            self.db.commit()
            self.close()
        except Exception as e:
            self.db.rollback()
            count = 0
        return count


    def run_sql(self,sql):
        # res = None
        try:
            self.connet()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.close()
        except Exception:
            res = None
        return res
    def cat_max_connections(self):
        """
        看当前的最大连接数
        默认是151个,最大连接数可以修改为16384
        """
        sql="show variables like 'max_connections';"
        data=self.run_sql(sql)
        return data

    def cat_variables(self):
        """
        查看数据库所有配置
        """
        sql="show global variables;"
        data=self.run_sql(sql)
        return data

class Bruce_mysql_pool:
    def __init__(self,host='localhost', port=3306,password="123456"):
        # 创建连接池
        self.host = host
        self.port = port
        self.password = password
        self.pool = self._create_pool()
    def _create_pool(self):
        return PooledDB(
            creator=pymysql, # 使用数据库的模块
            maxconnections=5,  # 设置最大连接数量
            mincached=2,  # 设置初始空闲连接数量
            maxcached=3,  # 连接池中最多可以存放的空闲连接数量
            blocking=True,  # 连接池中没有空闲连接后设置是否等待，True等待，False不等待
            host='localhost',  # 数据库主机地址
            port=3306,  # 数据库端口
            ping=0,# #检查服务是否可用
            # # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            user='root',  # 数据库用户名
            password='123456',  # 数据库密码
            #database='test'  # 默认连接的数据库
        )

    def create_mysql_client(self):
        """
        连接池中拿一个连接，自动回收连接
        """
        # 获取Mysql连接
        conn = Bruce_mysql(self.pool)
        return conn


class Mysql_mock_error:
    def mock_client_max(self, host='localhost', port=3306, user="root", max_connections=148, password="123456"):
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
                connection =  pymysql.connect(host=host,
                                      port=port,
                                      user=user,
                                      password=password,
                                      use_unicode=True,
                                      charset='utf8')

                connection.commit()
                connections.append(connection)
            time.sleep(10000)
        except pymysql.err.OperationalError as eroor:
            print("mysql连接数已经达到最大值,不能连接了", eroor)
        except Exception as e:
            print("e", e)

#
# Mysql_mock_error().mock_client_max()