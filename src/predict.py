import sqlite3
import joblib

DB_NAME = "machine_data.db"
MODEL_PATH = "models/machine_fault_model.pkl"

# Load ML model
model = joblib.load(MODEL_PATH)

# Connect to database
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Get latest sensor data
cursor.execute("""
    SELECT timestamp, temperature, vibration, current, rpm
    FROM sensor_data
    ORDER BY id DESC
    LIMIT 1
""")

row = cursor.fetchone()
conn.close()

if row is None:
    print("No sensor data found.")
    exit()

timestamp, temperature, vibration, current, rpm = row

# Prepare data for prediction
features = [[temperature, vibration, current, rpm]]

# Predict machine condition
prediction = model.predict(features)[0]

print("\n--- Machine Health Prediction ---")
print("Timestamp   :", timestamp)
print("Temperature :", temperature, "°C")
print("Vibration   :", vibration, "g")
print("Current     :", current, "A")
print("RPM         :", rpm)
print("Prediction  :", prediction)

# Alert
if prediction == "FAULT":
    print("\nALERT: MACHINE FAULT DETECTED!")
elif prediction == "WARNING":
    print("\nWARNING: MACHINE CONDITION NEEDS ATTENTION!")
else:
    print("\nMachine condition is NORMAL.")