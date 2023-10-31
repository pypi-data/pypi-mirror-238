#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Class that handles sqlite database operations.
"""

import sqlite3

from wotpy.database.database_schema import DB_SCHEMA

class SQLiteDatabase:
    """Class that handles all sqlite database operations"""

    def __init__(self, db_path):
        self.db_path = db_path if db_path is not None else "vo.db"
        self.conn = sqlite3.connect(self.db_path)
        self.conn.executescript(DB_SCHEMA)
        self.conn.commit()

    def execute_query(self, query):
        """Execute the provided SQL query on the database and return the result"""

        cursor = self.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def insert_data(self, table_name, data):
        """Insert the provided data into the specified table"""

        cursor = self.conn.cursor()
        placeholders = ",".join(["?" for i in range(len(data))])
        query = f"INSERT OR REPLACE INTO {table_name} VALUES ({placeholders})"
        cursor.execute(query, data)
        self.conn.commit()
        cursor.close()

    #TODO: add get, create methods for the database