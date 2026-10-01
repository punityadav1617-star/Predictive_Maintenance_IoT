import sqlite3

DB_NAME = "machine_data.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    temperature REAL,
    vibration REAL,
    current REAL,
    rpm REAL,
    status TEXT
)
""")

conn.commit()
conn.close()

print("SQLite database created successfully!")
print("Database: machine_data.db")