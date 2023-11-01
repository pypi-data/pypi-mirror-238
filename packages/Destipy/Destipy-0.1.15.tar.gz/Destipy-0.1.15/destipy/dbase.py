"""This file contains the context manager for the sqlite3 database connection.

Note:
    This file is from the pydest library:
    https://github.com/jgayfer/pydest/blob/master/pydest/dbase.py
"""
import sqlite3


class DBase:
    """
    The context manager for the sqlite3 database connection.
    """
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def query(self, hash_id, definition, identifier):
        sql = """
              SELECT json FROM {}
              WHERE {} = {}
              """
        self.cur.execute(sql.format(definition, identifier, hash_id))
        return self.cur.fetchall()
