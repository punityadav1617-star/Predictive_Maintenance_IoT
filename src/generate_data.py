import sqlite3
import random
from datetime import datetime, timedelta

DB_NAME = "machine_data.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

start_time = datetime.now()

for i in range(2000):

    temperature = random.gauss(35, 2)
    vibration = random.gauss(0.25, 0.05)
    current = random.gauss(0.8, 0.08)
    rpm = random.gauss(1450, 30)

    fault_probability = random.random()

    if fault_probability < 0.10:
        temperature += random.uniform(10, 20)
        vibration += random.uniform(0.6, 1.2)
        current += random.uniform(0.4, 0.8)
        rpm -= random.uniform(150, 300)
        status = "FAULT"

    elif fault_probability < 0.20:
        temperature += random.uniform(4, 10)
        vibration += random.uniform(0.2, 0.5)
        current += random.uniform(0.1, 0.3)
        rpm -= random.uniform(50, 150)
        status = "WARNING"

    else:
        status = "NORMAL"

    timestamp = start_time + timedelta(seconds=i)

    cursor.execute("""
        INSERT INTO sensor_data
        (timestamp, temperature, vibration, current, rpm, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        timestamp.isoformat(),
        round(temperature, 2),
        round(vibration, 3),
        round(current, 2),
        round(rpm, 2),
        status
    ))

conn.commit()
conn.close()

print("Synthetic sensor data inserted into SQLite successfully!")
print("Total records: 2000")