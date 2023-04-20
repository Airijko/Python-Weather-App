import sqlite3

class DBOperations:
    def __init__(self, db_path):
        self.db_path = db_path

    def fetch_data(self, location, start_date, end_date):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT sample_date, min_temp, max_temp, avg_temp
                              FROM weather_data
                              WHERE location = ? AND sample_date BETWEEN ? AND ?
                              ORDER BY sample_date''', (location, start_date, end_date))
            rows = cursor.fetchall()
            return rows

    def save_data(self, data):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for row in data:
                sample_date, location, min_temp, max_temp, avg_temp = row
                cursor.execute('''INSERT OR IGNORE INTO weather_data
                                  (sample_date, location, min_temp, max_temp, avg_temp)
                                  VALUES (?, ?, ?, ?, ?)''', (sample_date, location, min_temp, max_temp, avg_temp))
            conn.commit()

    def initialize_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS weather_data
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            sample_date TEXT UNIQUE,
                            location TEXT,
                            min_temp REAL,
                            max_temp REAL,
                            avg_temp REAL)''')
            conn.commit()


    def purge_data(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('DELETE FROM weather_data')
            conn.commit()
