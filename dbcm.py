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
        """initialize the class."""
        self.db_file = db_file
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        self.conn.close()
