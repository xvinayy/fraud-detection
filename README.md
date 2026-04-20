# 💳 Real-Time Fraud Detection System

## 🚀 Overview

This project is a **rule-based real-time fraud detection system** built using **Python and Streamlit**.
It simulates transaction monitoring and detects fraudulent activities based on predefined rules.

The system provides a **live dashboard** that processes transactions, assigns a fraud score, and displays alerts with explanations.

---

## 🎯 Features

* ✅ Real-time transaction simulation
* 🚨 Fraud detection using multiple rules
* 📊 Interactive dashboard (Streamlit UI)
* 🔢 Fraud score (0–100) for each transaction
* 📍 Detection based on:

  * High transaction amount
  * Rapid transaction frequency
  * Location changes
  * Unusual transaction time
  * New device detection
* 📜 Transaction history tracking
* ⚡ Live fraud alert panel

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **Pandas**

---

## 🧠 How It Works

The system uses a **rule-based approach**:

Each transaction is evaluated against multiple conditions:

* If amount exceeds a threshold → flagged
* If too many transactions occur in a short time → flagged
* If location suddenly changes → flagged
* If transaction occurs at odd hours → flagged

A **fraud score** is calculated based on triggered rules.

---

## ▶️ How to Run

1. Clone the repository:

```bash
git clone https://github.com/your-username/fraud-detection.git
```

2. Navigate to the project folder:

```bash
cd fraud-detection
```

3. Install dependencies:

```bash
pip install streamlit pandas
```

4. Run the app:

```bash
python -m streamlit run fraud_detection.py
```

---

## 📸 Demo

* Click **Start Monitoring**
* Watch transactions generate in real-time
* Fraudulent transactions appear in the alert panel

---

## 📌 Future Improvements

* 🔗 Integration with real-time APIs
* 🧠 Machine learning-based fraud detection
* 🗄️ Database integration
* 🔐 User authentication system
* 📈 Advanced analytics and graphs

---

## 👨‍💻 Author

Developed as part of a **Data Analytics and Algorithms (DAA)** project.

---

## ⭐ Note

This project is for educational purposes and demonstrates the concept of fraud detection using rule-based logic.
