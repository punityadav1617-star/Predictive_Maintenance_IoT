import sqlite3
import random
import time
from datetime import datetime

DB_NAME = "machine_data.db"

print("Live sensor simulation started...")
print("Press CTRL+C to stop.\n")

while True:

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

    elif fault_probability < 0.20:
        temperature += random.uniform(4, 10)
        vibration += random.uniform(0.2, 0.5)
        current += random.uniform(0.1, 0.3)
        rpm -= random.uniform(50, 150)

    timestamp = datetime.now().isoformat()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sensor_data
        (timestamp, temperature, vibration, current, rpm, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        round(temperature, 2),
        round(vibration, 3),
        round(current, 2),
        round(rpm, 2),
        "LIVE"
    ))

    conn.commit()
    conn.close()

    print(
        f"Temperature: {temperature:.2f} °C | "
        f"Vibration: {vibration:.2f} g | "
        f"Current: {current:.2f} A | "
        f"RPM: {rpm:.2f}"
    )

    time.sleep(2)