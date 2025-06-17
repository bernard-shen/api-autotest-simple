#-*- coding: utf-8 -*-
from pymysql import *
from dbutils.pooled_db import PooledDB
import sqlite3
from loguru import logger
import time
import os


'''单连接'''
class MysqlClass():

    def __init__(self,host,port,db,user,password):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password
        self.connect = connect(host=self.host, port=self.port, db=self.db,user=self.user,password=self.password,charset='utf8')
        self.cursor = self.connect.cursor()
        self.nowTime = time.strftime("%Y-%m-%d", time.localtime())
        logger.add("log/file_{}.log".format(self.nowTime))

    def getData(self,sql):
        try:
           self.cursor.execute(sql)
        except DatabaseError as e:
            logger.error('db err:{}'.format(e))
        finally:
            # 关闭游标
            self.cursor.close()
            # 关闭连接
            # self.connect.close()
        return self.cursor.fetchone()

    def getDataMany(self,sql):
        try:
           self.cursor.execute(sql)
        except DatabaseError as e:
            logger.error('db err:{}'.format(e))
        finally:
            # 关闭游标
            self.cursor.close()
            # 关闭连接
            # self.connect.close()
        return self.cursor.fetchall()

    def addDataOne(self,sql):
        try:
           self.cursor.execute(sql)
        except DatabaseError as e:
            logger.error('db err:{}'.format(e))
        finally:
            # 关闭游标
            self.cursor.close()
            # 关闭连接
            self.connect.close()
        return self.cursor.fetchall()


    def addDataMany(self,sql,params):
        try:
           self.cursor.executemany(sql,params)
        except DatabaseError as e:
            logger.error('db err:{}'.format(e))
        finally:
            # 关闭游标
            self.cursor.close()
            # 关闭连接
            self.connect.close()
        return self.cursor.fetchall()

    def modifyData(self,sql):
        try:
           self.cursor.execute(sql)
           self.cursor.commit()
        except DatabaseError as e:
            logger.error('db err:{}'.format(e))
        finally:
            # 关闭游标
            self.cursor.close()
            # 关闭连接
            self.connect.close()
        return self.cursor.fetchall()

    def modifyDataMany(self,sql,params):
        try:
           self.cursor.executemany(sql,params)
           self.cursor.commit()
        except DatabaseError as e:
            logger.error('db err:{}'.format(e))
        finally:
            # 关闭游标
            self.cursor.close()
            # 关闭连接
            self.connect.close()
        return self.cursor.fetchall()

    def delData(self,sql):
        try:
           self.cursor.execute(sql)
           self.cursor.commit()
        except DatabaseError as e:
            logger.error('db err:{}'.format(e))
        finally:
            # 关闭游标
            self.cursor.close()
            # 关闭连接
            self.connect.close()
        return self.cursor.fetchall()

    def delDataMany(self,sql,params):
        try:
           self.cursor.executemany(sql,params)
           self.cursor.commit()
        except DatabaseError as e:
            logger.error('db err:{}'.format(e))
        finally:
            # 关闭游标
            self.cursor.close()
            # 关闭连接
            self.connect.close()
        return self.cursor.fetchall()


'''使用链接池'''
class MysqlPoolClass():
    def __init__(self, host, port, db, user, password, maxconnections=10):
        """
        初始化数据库连接池
        :param host: 数据库主机地址
        :param port: 数据库端口
        :param db: 数据库名
        :param user: 用户名
        :param password: 密码
        :param maxconnections: 最大连接数，默认10
        """
        self.pool = PooledDB(
            creator=connect,  # 使用pymysql作为数据库连接器
            maxconnections=maxconnections,  # 连接池最大连接数
            mincached=2,  # 初始化时，连接池中至少创建的空闲的链接
            maxcached=5,  # 连接池中最多闲置的链接
            maxshared=3,  # 链接最大共享数
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表
            ping=0,  # ping MySQL服务端，检查是否服务可用
            host=host,
            port=port,
            db=db,
            user=user,
            password=password,
            charset='utf8'
        )
        self.nowTime = time.strftime("%Y-%m-%d", time.localtime())
        logger.add("log/file_{}.log".format(self.nowTime))

    def get_connection(self):
        """获取数据库连接"""
        return self.pool.connection()

    def execute_query(self, sql, params=None):
        """
        执行查询操作
        :param sql: SQL语句
        :param params: 参数
        :return: 查询结果
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except DatabaseError as e:
            logger.error('db err:{}'.format(e))
            return None
        finally:
            cursor.close()
            conn.close()

    def execute_one(self, sql, params=None):
        """
        执行查询操作，返回单条记录
        :param sql: SQL语句
        :param params: 参数
        :return: 查询结果
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            result = cursor.fetchone()
            return result
        except DatabaseError as e:
            logger.error('db err:{}'.format(e))
            return None
        finally:
            cursor.close()
            conn.close()

    def execute_many(self, sql, params_list):
        """
        批量执行SQL语句
        :param sql: SQL语句
        :param params_list: 参数列表
        :return: 影响行数
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.executemany(sql, params_list)
            conn.commit()
            return cursor.rowcount
        except DatabaseError as e:
            conn.rollback()
            logger.error('db err:{}'.format(e))
            return 0
        finally:
            cursor.close()
            conn.close()

    def execute_update(self, sql, params=None):
        """
        执行更新操作
        :param sql: SQL语句
        :param params: 参数
        :return: 影响行数
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            conn.commit()
            return cursor.rowcount
        except DatabaseError as e:
            conn.rollback()
            logger.error('db err:{}'.format(e))
            return 0
        finally:
            cursor.close()
            conn.close()


class SQLiteConnector:
    def __init__(self, db_path):
        """
        初始化SQLite数据库连接
        :param db_path: 数据库文件路径
        """
        self.db_path = db_path
        self.nowTime = time.strftime("%Y-%m-%d", time.localtime())
        logger.add("log/file_{}.log".format(self.nowTime))


    def get_connection(self):
        """
        获取数据库连接
        :return: 数据库连接
        """
        try:
            # 确保数据库目录存在
            db_dir = os.path.dirname(self.db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)
            
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            logger.error(f"数据库连接错误: {e}")
            return None

    def execute_query(self, sql, params=None):
        """
        执行查询操作
        :param sql: SQL查询语句
        :param params: 查询参数
        :return: 查询结果
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"查询执行错误: {e}")
            return None

    def execute_one(self, sql, params=None):
        """
        执行查询操作，返回单条记录
        :param sql: SQL查询语句
        :param params: 查询参数
        :return: 单条查询结果
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                return cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f"查询执行错误: {e}")
            return None

    def execute_update(self, sql, params=None):
        """
        执行更新操作（插入、更新、删除）
        :param sql: SQL更新语句
        :param params: 更新参数
        :return: 影响的行数
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                conn.commit()
                return cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f"更新执行错误: {e}")
            return 0

    def create_table(self, table_name, columns):
        """
        创建数据表
        :param table_name: 表名
        :param columns: 列定义，例如: "id INTEGER PRIMARY KEY, name TEXT, age INTEGER"
        :return: 是否创建成功
        """
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql)
                conn.commit()
                return True
        except sqlite3.Error as e:
            logger.error(f"创建表错误: {e}")
            return False



