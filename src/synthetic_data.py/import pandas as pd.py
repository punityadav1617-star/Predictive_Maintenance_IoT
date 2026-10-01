try:
    import pandas as pd  # type: ignore[import-not-found]
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError("pandas is required to run this synthetic data generator. Install it with: pip install pandas") from exc

try:
    import numpy as np  # type: ignore[import-not-found]
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError("numpy is required to run this synthetic data generator. Install it with: pip install numpy") from exc
from datetime import datetime, timedelta

np.random.seed(42)

records = 2000
data = []

start_time = datetime.now()

for i in range(records):

    # Normal operating values
    temperature = np.random.normal(35, 2)
    vibration = np.random.normal(0.25, 0.05)
    current = np.random.normal(0.8, 0.08)
    rpm = np.random.normal(1450, 30)

    # Introduce machine faults randomly
    fault_probability = np.random.random()

    if fault_probability < 0.10:
        # Fault condition
        temperature += np.random.uniform(10, 20)
        vibration += np.random.uniform(0.6, 1.2)
        current += np.random.uniform(0.4, 0.8)
        rpm -= np.random.uniform(150, 300)
        status = "FAULT"

    elif fault_probability < 0.20:
        # Warning condition
        temperature += np.random.uniform(4, 10)
        vibration += np.random.uniform(0.2, 0.5)
        current += np.random.uniform(0.1, 0.3)
        rpm -= np.random.uniform(50, 150)
        status = "WARNING"

    else:
        status = "NORMAL"

    timestamp = start_time + timedelta(seconds=i)

    data.append([
        timestamp,
        round(temperature, 2),
        round(vibration, 3),
        round(current, 2),
        round(rpm, 2),
        status
    ])

# Create DataFrame
df = pd.DataFrame(data, columns=[
    "Timestamp",
    "Temperature_C",
    "Vibration_g",
    "Current_A",
    "RPM",
    "Status"
])

# Save CSV
df.to_csv("machine_sensor_data.csv", index=False)

print("Synthetic IoT dataset generated successfully!")
print(f"Total records: {len(df)}")
print("\nFirst 10 records:")
print(df.head(10))

print("\nStatus distribution:")
print(df["Status"].value_counts())