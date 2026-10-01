import sqlite3
import paho.mqtt.client as mqtt
import json
import time

DB_NAME = "machine_data.db"

# ==============================
# HiveMQ Cloud
# ==============================

BROKER = "df72892d2dc14f5e9fe03b046468a982.s1.eu.hivemq.cloud"
PORT = 8883
TOPIC = "machine/sensor_data"

USERNAME = "Punit yadav"
PASSWORD = "@punit1234"


# ==============================
# SQLite database connect
# ==============================

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()


# ==============================
# MQTT client
# ==============================

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

# HiveMQ username/password
client.username_pw_set(
    USERNAME,
    PASSWORD
)

# Enable TLS
client.tls_set()


# ==============================
# Connect to HiveMQ
# ==============================

print("Connecting to HiveMQ Cloud...")

try:
    client.connect(BROKER, PORT, 60)
    print("Connected to HiveMQ Cloud!")
    print("Topic:", TOPIC)
    print("Reading sensor data from SQLite...\n")

except Exception as e:
    print("Connection failed!")
    print("Error:", e)

    conn.close()
    exit()


# ==============================
# Read data from SQLite
# ==============================

cursor.execute("""
    SELECT timestamp, temperature, vibration, current, rpm, status
    FROM sensor_data
    ORDER BY id
""")

rows = cursor.fetchall()


# ==============================
# Publish data
# ==============================

for row in rows:

    data = {
        "timestamp": row[0],
        "temperature": row[1],
        "vibration": row[2],
        "current": row[3],
        "rpm": row[4],
        "status": row[5]
    }

    message = json.dumps(data)

    result = client.publish(
        TOPIC,
        message,
        qos=1
    )

    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print("Sent:", message)
    else:
        print("Failed:", message)

    time.sleep(1)


# ==============================
# Close connections
# ==============================

conn.close()
client.disconnect()

print("\nAll sensor data sent to HiveMQ successfully!")