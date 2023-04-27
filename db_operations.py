"""
Class:
- DBOperations: performs database operations.

Usage:
create an instance of DBOperations
db = DBOperations('weather_data.db')
"""

from dbcm import DBCM

# TEST

class DBOperations:
    """This class is used to perform database operations."""
    def __init__(self, db_path="weather.sqlite"):
        """initialize the class."""
        self.db_path = db_path

    def fetch_data(self, start_date, end_date):
        """This function is used to fetch the data from the database."""
        with DBCM(self.db_path) as conn:
            conn.execute('''SELECT * FROM weather_data
                            WHERE sample_date >= ? 
                            AND sample_date <= ?
                            ORDER by sample_date;''',
                            (start_date, end_date))
            return conn.fetchall()

    def save_data(self, data):
        """This function is used to save the data to the database."""
        with DBCM(self.db_path) as conn:
            for row in data:
                min_temp = float(row[1]) if row[1] else None
                max_temp = float(row[2]) if row[2] else None
                avg_temp = float(row[3]) if row[3] else None
                sample_date, location = row[0], 'location_name'
                conn.execute('''INSERT OR IGNORE INTO weather_data
                                (sample_date, location, min_temp, max_temp, avg_temp)
                                VALUES (?, ?, ?, ?, ?)''',
                                (sample_date, location, min_temp, max_temp, avg_temp))

    def initialize_db(self):
        """This function is used to initialize the database."""
        with DBCM(self.db_path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS weather_data
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            sample_date TEXT UNIQUE,
                            location TEXT,
                            min_temp REAL,
                            max_temp REAL,
                            avg_temp REAL)''')

    def purge_data(self):
        """This function is used to purge the database."""
        with DBCM(self.db_path) as conn:
            conn.execute('DELETE FROM weather_data')

    def get_all_data(self):
        """This function is used to get all the data from the database."""
        with DBCM(self.db_path) as conn:
            query = "SELECT * FROM weather_data"
            conn.execute(query)
            return conn.fetchall()