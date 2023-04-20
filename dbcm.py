"""
Classes:
- DBCM: A context manager that provides a connection to a SQLite database.
"""

import sqlite3

class DBCM:
    """
    DBCM is a context manager that provides a connection to a database.
    """
    def __init__(self, db_path):
        self.db_path = db_path

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.conn.rollback() #rollback changes
        else:
            self.conn.commit() # commit changes
        self.conn.close()
