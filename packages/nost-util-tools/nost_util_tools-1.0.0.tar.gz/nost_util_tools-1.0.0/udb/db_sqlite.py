# -*- coding: utf-8 -*-
"""
@Author : zhang.yonggang
@File   : db_sqlite.py
@Project: py_util_tools
@Time   : 2023-10-27 16:42:42
@Desc   : This file contains some commonly used classes and methods for SQLite operations.
@Version: v1.0
"""
import logging
import sqlite3

logger = rootLogger = logging.getLogger(__name__)


class SqliteDatabase:
    """
    Sqlite数据库类
    """

    def __init__(self, path, init_table_list=[]):
        """
        init sqlite
        :param path: db path
        :param init_table_list: A list of SQL statements for initializing tables is needed for creating a new database.
        """
        self.__db_path = path
        self.conn = None
        self.cursor = None
        self.connect()
        # init table
        for init_table in init_table_list:
            self.cursor.execute(init_table)
        self.conn.commit()
        self.dis_connect()

    def connect(self):
        self.conn = sqlite3.connect(self.__db_path)
        self.cursor = self.conn.cursor()

    def dis_connect(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.conn:
            self.conn.close()
            self.conn = None

    def insert_info(self, sql, params=None):
        """
        insert
        :param params: Insertion parameters, optional.
        :param sql: insert sql
        :return: insert id
        :params example:
            # Define the data to be inserted
            data = OrderedDict([
                ('name', 'John'),
                ('age', 25),
                ('city', 'New York')
            ])

            # Construct the SQL statement for insertion.
            sql = "INSERT INTO your_table (name, age, city) VALUES (?, ?, ?)"
            params = tuple(data.values())
        """
        if self.conn is None:
            self.connect()
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        insert_id = self.cursor.lastrowid
        self.conn.commit()
        self.dis_connect()
        return insert_id

    def delete_info(self, sql, params=None):
        """
        update or delete
        :param sql: update or delete sql
        :param params: Insertion parameters, optional.
        :params example:
            # Define the data to be updated
            condition = OrderedDict([
                ('id', 1)
            ])

            # Construct the SQL statement for delete.
            sql = "DELETE FROM your_table WHERE "
            sql += " AND ".join("{} = ?".format(field) for field in condition.keys())
            params = tuple(condition.values())

            # Define the data to be updated and the conditions.
            data = OrderedDict([
                ('name', 'John Smith'),
                ('age', 30)
            ])
            condition = OrderedDict([
                ('id', 1)
            ])

            # Construct the SQL statement for update.
            sql = "UPDATE your_table SET "
            sql += ", ".join("{} = ?".format(field) for field in data.keys())
            sql += " WHERE "
            sql += " AND ".join("{} = ?".format(field) for field in condition.keys())
            params = tuple(data.values()) + tuple(condition.values())
        """
        if self.conn is None:
            self.connect()
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        self.conn.commit()
        self.dis_connect()

    update_info = delete_info

    def get_select_results(self, sql, params=None):
        """
        select all dates from db
        :param sql: sql
        :param params: Insertion parameters, optional.
        :return: list of all results, the type is dict in list, key is column name, value is column value
        :params example:
            # Define the data to be selected and the conditions.
            condition = OrderedDict([
                ('age', 25),
                ('city', 'New York')
            ])

            # Construct the SQL statement for select.
            sql = "SELECT * FROM your_table WHERE "
            sql += " AND ".join("{} = ?".format(field) for field in condition.keys())
            params = tuple(condition.values())
        """
        self.connect()
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            # select all date
            results = self.cursor.fetchall()
            if results:
                result_list = []
                columns = [column[0] for column in self.cursor.description]
                for row in results:
                    # covert result to dict
                    row_dict = dict(zip(columns, row))
                    result_list.append(row_dict)
                return result_list
        except:
            rootLogger.exception(f"execute {sql} error")
        finally:
            self.dis_connect()

    def get_select_single_result(self, sql, is_disconnect=True, params=None):
        """
        执行SQL, 获取单条记录
        :param is_disconnect: 默认查询后关闭数据库连接
        :param sql: sql语句
        :param params: 参数, 可用可不用
        :return: 单条记录的dict(key为字段名称, value为字段值)
        :params example:
            # 定义查询的条件
            condition = OrderedDict([
                ('age', 25),
                ('city', 'New York')
            ])

            # 构造查询的 SQL 语句
            sql = "SELECT * FROM your_table WHERE "
            sql += " AND ".join("{} = ?".format(field) for field in condition.keys())
            params = tuple(condition.values())
        """
        if not self.conn:
            self.connect()
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            # 获取查询结果
            result = self.cursor.fetchone()
            if result:
                columns = [column[0] for column in self.cursor.description]
                result_dict = dict(zip(columns, result))
                return result_dict
        except:
            rootLogger.exception(f"execute {sql} error")
        finally:
            if is_disconnect:
                self.dis_connect()
