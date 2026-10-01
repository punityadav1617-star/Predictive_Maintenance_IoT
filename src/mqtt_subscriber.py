import sqlite3
import json
import paho.mqtt.client as mqtt

DB_NAME = "machine_data.db"

BROKER = "localhost"
PORT = 1883
TOPIC = "machine/sensor_data"


def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to MQTT Broker!")
    client.subscribe(TOPIC)
    print("Subscribed to:", TOPIC)

def on_message(client, userdata, msg):

    data = json.loads(msg.payload.decode())

    print("Received:", data)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sensor_data
        (timestamp, temperature, vibration, current, rpm, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["timestamp"],
        data["temperature"],
        data["vibration"],
        data["current"],
        data["rpm"],
        data["status"]
    ))

    conn.commit()
    conn.close()

    print("Saved to SQLite!")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

print("Waiting for sensor data...\n")

client.loop_forever()