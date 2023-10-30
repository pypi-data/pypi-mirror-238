# -*- coding: utf-8 -*-
"""
@Author : zhang.yonggang
@File   : db_postgresql.py
@Project: py_util_tools
@Time   : 2023-10-27 15:27:18
@Desc   : This file contains some commonly used classes and methods for Postgresql operations.
@Version: v1.0
"""
import logging

from sqlalchemy import create_engine, text

logger = rootLogger = logging.getLogger(__name__)


class PostgresqlDatabase:
    def __init__(self, db_url) -> None:
        """
        :param db_url: postgresql://username:password@host:port/db_name
        """
        logger.info(f"init db {db_url}")
        self.engine = create_engine(db_url)

    def execute_query(self, query_sql) -> tuple[list[str], list[str]]:
        logger.info(f"execute sql {query_sql}")
        with self.engine.connect() as conn:
            result = conn.execute(text(query_sql))
            columns = result.keys()
            rows = result.fetchall()
            return columns, rows

    def execute_update(self, query_sql) -> None:
        logger.info(f"execute sql {query_sql}")
        with self.engine.connect() as conn:
            conn.execute(text(query_sql))
            conn.commit()

    def execute_insert(self, query_sql) -> str:
        """
        execute insert
        :param query_sql: sql
        :return: id of inserted
        """
        logger.info(f"execute insert sql {query_sql}")
        with self.engine.connect() as conn:
            result = conn.execute(text(query_sql))
            conn.commit()
            return result.lastrowid

    execute_delete = execute_update

    def fetch_one(self, query_sql) -> dict:
        """
        select only one date from db
        :param query_sql: sql
        :return: dict of one result, key is column name, value is column value,
                if it has no result, return None
        """
        columns, rows = self.execute_query(query_sql)
        if rows:
            row = rows[0]
            return {column: row[index] for index, column in enumerate(columns)}
        else:
            return None

    def fetch_all(self, query_sql) -> list[dict]:
        """
        select all dates from db
        :param query_sql: sql
        :return: list of all results, the type is dict in list, key is column name, value is column value
        """
        columns, rows = self.execute_query(query_sql)
        results = []
        for row in rows:
            result = {column: row[index] for index, column in enumerate(columns)}
            results.append(result)
        return results
