import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import time

# -------------------------------
# Page Config + Styling
# -------------------------------
st.set_page_config(page_title="Fraud Detection Dashboard", layout="wide")

st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.main {
    background-color: #0e1117;
    color: white;
}
h1 {
    text-align: center;
    color: #00ffd5;
}
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
}
.fraud {
    background-color: #ff4b4b;
    padding: 20px;
    border-radius: 15px;
}
.safe {
    background-color: #00c896;
    padding: 20px;
    border-radius: 15px;
}
.stButton>button {
    background: linear-gradient(90deg, #00ffd5, #00c2a8);
    color: black;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>💳 AI Fraud Detection Dashboard</h1>", unsafe_allow_html=True)
st.markdown("### 📡 Real-Time Transaction Monitoring")

# -------------------------------
# Fraud Detection Logic
# -------------------------------
class FraudDetector:
    def __init__(self):
        self.user_profiles = {}

    def process_transaction(self, tx):
        user_id = tx['user_id']
        amount = tx['amount']
        loc = tx['location']
        tx_time = tx['time']
        device_id = tx['device_id']

        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                'tx_timestamps': [],
                'known_devices': set(),
                'last_location': loc
            }

        profile = self.user_profiles[user_id]
        reasons = []
        status = "APPROVED"
        score = 0

        if amount > 50000:
            status = "FRAUD"
            score += 40
            reasons.append("High amount")

        one_min_ago = tx_time - timedelta(minutes=1)
        recent_txs = [t for t in profile['tx_timestamps'] if t >= one_min_ago]
        if len(recent_txs) >= 3:
            status = "FRAUD"
            score += 30
            reasons.append("High frequency")

        if len(profile['tx_timestamps']) > 0 and profile['last_location'] != loc:
            status = "FRAUD"
            score += 20
            reasons.append("Location change")

        if 1 <= tx_time.hour <= 4 and amount > 10000:
            status = "FRAUD"
            score += 25
            reasons.append("Odd hour transaction")

        if len(profile['known_devices']) > 0 and device_id not in profile['known_devices']:
            if status != "FRAUD":
                status = "SUSPICIOUS"
            score += 15
            reasons.append("New device")

        if amount > 20000 and profile['last_location'] != loc:
            status = "FRAUD"
            score += 20
            reasons.append("Unusual location spending")

        profile['tx_timestamps'].append(tx_time)
        profile['known_devices'].add(device_id)
        profile['last_location'] = loc

        return status, reasons, score

# -------------------------------
# Generate Transactions
# -------------------------------
def generate_transaction():
    return {
        "user_id": random.choice(["U001", "U002", "U003"]),
        "amount": random.randint(100, 70000),
        "location": random.choice(["India", "USA", "UK", "Dubai"]),
        "time": datetime.now(),
        "device_id": random.choice(["D1", "D2", "D3"])
    }

# -------------------------------
# Initialize
# -------------------------------
if "detector" not in st.session_state:
    st.session_state.detector = FraudDetector()

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# Button
# -------------------------------
if st.button("🚀 Start Monitoring"):
    for _ in range(10):
        tx = generate_transaction()
        status, reasons, score = st.session_state.detector.process_transaction(tx)

        st.session_state.history.append({
            "User": tx["user_id"],
            "Amount": tx["amount"],
            "Location": tx["location"],
            "Time": tx["time"].strftime("%H:%M:%S"),
            "Status": status,
            "Score": score,
            "Reason": ", ".join(reasons)
        })

        time.sleep(0.8)

# -------------------------------
# Layout
# -------------------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📊 Transaction History")
    df = pd.DataFrame(st.session_state.history)
    if not df.empty:
        st.dataframe(df, use_container_width=True)

with col2:
    st.markdown("### 🚨 Live Alerts")

    frauds = [tx for tx in st.session_state.history if tx["Status"] == "FRAUD"]

    if frauds:
        latest = frauds[-1]

        st.markdown(f"""
        <div class="fraud">
            <h3>🚨 FRAUD DETECTED</h3>
            <p><b>User:</b> {latest['User']}</p>
            <p><b>Amount:</b> ₹{latest['Amount']}</p>
            <p><b>Score:</b> {latest['Score']}</p>
            <p><b>Reasons:</b> {latest['Reason']}</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="safe">
            <h3>✅ No Fraud Detected</h3>
        </div>
        """, unsafe_allow_html=True)