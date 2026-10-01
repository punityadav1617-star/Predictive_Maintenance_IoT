import sqlite3
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

DB_NAME = "machine_data.db"
MODEL_PATH = "models/machine_fault_model.pkl"

# Database connect
conn = sqlite3.connect(DB_NAME)

query = """
SELECT temperature, vibration, current, rpm, status
FROM sensor_data
"""

data = conn.execute(query).fetchall()
conn.close()

# Features and target
X = []
y = []

for row in data:
    temperature, vibration, current, rpm, status = row

    X.append([temperature, vibration, current, rpm])
    y.append(status)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Create model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Test
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Model training completed!")
print(f"Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Create models folder if needed
os.makedirs("models", exist_ok=True)

# Save model
joblib.dump(model, MODEL_PATH)

print(f"\nModel saved successfully at: {MODEL_PATH}")