import streamlit as st
from datetime import datetime, timedelta

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

        # Rule 1
        if amount > 50000:
            status = "FRAUD"
            reasons.append("High transaction amount")

        # Rule 2
        one_min_ago = tx_time - timedelta(minutes=1)
        recent_txs = [t for t in profile['tx_timestamps'] if t >= one_min_ago]
        if len(recent_txs) >= 3:
            status = "FRAUD"
            reasons.append("Too many transactions in short time")

        # Rule 3
        if len(profile['tx_timestamps']) > 0 and profile['last_location'] != loc:
            status = "FRAUD"
            reasons.append(f"Location changed from {profile['last_location']} to {loc}")

        # Rule 4
        hour = tx_time.hour
        if 1 <= hour <= 4 and amount > 10000:
            status = "FRAUD"
            reasons.append("High amount at unusual time")

        # Rule 5
        if len(profile['known_devices']) > 0 and device_id not in profile['known_devices']:
            if status != "FRAUD":
                status = "SUSPICIOUS"
            reasons.append(f"New device: {device_id}")

        # Custom Rule
        if amount > 20000 and profile['last_location'] != loc:
            status = "FRAUD"
            reasons.append("Unusual high spending in new location")

        # Update profile
        profile['tx_timestamps'].append(tx_time)
        profile['tx_timestamps'] = [t for t in profile['tx_timestamps'] if t >= tx_time - timedelta(minutes=5)]
        profile['known_devices'].add(device_id)
        profile['last_location'] = loc

        return status, reasons


# -------------------------------
# Streamlit UI
# -------------------------------
st.title("💳 Real-Time Fraud Detection System")

st.write("Enter transaction details below:")

user_id = st.text_input("User ID", "U001")
amount = st.number_input("Amount", min_value=0.0, value=100.0)
location = st.text_input("Location", "India")
device_id = st.text_input("Device ID", "D-01")

# Initialize detector (persistent across runs)
if "detector" not in st.session_state:
    st.session_state.detector = FraudDetector()

if st.button("Check Transaction"):
    tx = {
        "user_id": user_id,
        "amount": amount,
        "location": location,
        "time": datetime.now(),
        "device_id": device_id
    }

    status, reasons = st.session_state.detector.process_transaction(tx)

    st.subheader("Result:")

    if status == "FRAUD":
        st.error(f"🚨 FRAUD detected!\n\nReason: {', '.join(reasons)}")
    elif status == "SUSPICIOUS":
        st.warning(f"⚠️ SUSPICIOUS transaction\n\nReason: {', '.join(reasons)}")
    else:
        st.success("✅ Transaction Approved")