"""
Classes:
- DBCM: A context manager that provides a connection to a SQLite database.
"""

import sqlite3

class DBCM:
    """
    DBCM is a context manager that provides a connection to a database.
    """
    def __init__(self, db_file):
        self.db_file = db_file

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        self.conn.close()
