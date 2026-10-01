import streamlit as st
from streamlit_autorefresh import st_autorefresh
import sqlite3
import joblib
import pandas as pd

DB_NAME = "machine_data.db"
MODEL_PATH = "models/machine_fault_model.pkl"

st.set_page_config(
    page_title="Predictive Maintenance Dashboard",
    page_icon="⚙️",
    layout="wide"
)

# Auto refresh every 2 seconds
st_autorefresh(
    interval=2000,
    limit=None,
    key="machine_dashboard_refresh"
)

# Load ML model
model = joblib.load(MODEL_PATH)


def get_latest_data():
    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT timestamp, temperature, vibration, current, rpm
    FROM sensor_data
    ORDER BY id DESC
    LIMIT 1
    """

    data = pd.read_sql_query(query, conn)
    conn.close()

    return data


def get_recent_data():
    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT timestamp, temperature, vibration, current, rpm
    FROM sensor_data
    ORDER BY id DESC
    LIMIT 20
    """

    data = pd.read_sql_query(query, conn)
    conn.close()

    return data


# Get latest sensor data
latest = get_latest_data()

if latest.empty:
    st.error("No sensor data found in SQLite database.")
    st.stop()

temperature = latest.iloc[0]["temperature"]
vibration = latest.iloc[0]["vibration"]
current = latest.iloc[0]["current"]
rpm = latest.iloc[0]["rpm"]
timestamp = latest.iloc[0]["timestamp"]

# AI prediction
features = [[temperature, vibration, current, rpm]]
prediction = model.predict(features)[0]


# =========================
# DASHBOARD
# =========================

st.title("⚙️ Predictive Maintenance Dashboard")
st.subheader("Rotating Machinery — IoT + AI Monitoring")

st.write("🕒 Last Reading:", timestamp)

# Sensor cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🌡️ Temperature",
        f"{temperature:.2f} °C"
    )

with col2:
    st.metric(
        "📳 Vibration",
        f"{vibration:.2f} g"
    )

with col3:
    st.metric(
        "⚡ Current",
        f"{current:.2f} A"
    )

with col4:
    st.metric(
        "🔄 RPM",
        f"{rpm:.2f}"
    )


st.divider()


# =========================
# AI HEALTH STATUS
# =========================

st.subheader("🤖 AI Machine Health Prediction")

if prediction == "FAULT":

    st.error("🚨 MACHINE FAULT DETECTED!")

elif prediction == "WARNING":

    st.warning("⚠️ MACHINE CONDITION NEEDS ATTENTION!")

else:

    st.success("✅ MACHINE CONDITION IS NORMAL")


st.write("**Predicted Status:**", prediction)


st.divider()


# =========================
# RECENT DATA
# =========================

st.subheader("📊 Recent Sensor Data")

recent = get_recent_data()

st.dataframe(
    recent,
    use_container_width=True
)


# =========================
# SENSOR GRAPH
# =========================

st.subheader("📈 Sensor Trends")

chart_data = recent.sort_values("timestamp")

st.line_chart(
    chart_data.set_index("timestamp")[
        ["temperature", "vibration", "current", "rpm"]
    ]
)


st.divider()

st.caption(
    "🔄 Dashboard refreshes automatically every 2 seconds | "
    "Data Source: SQLite | AI Model: Random Forest"
)