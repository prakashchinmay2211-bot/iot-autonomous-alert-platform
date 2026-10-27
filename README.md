# ⚡ AIDAMS: Autonomous IoT Decision and Alert Management Platform

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![MQTT](https://img.shields.io/badge/MQTT-HiveMQ-660066?style=for-the-badge&logo=mqtt&logoColor=white)](https://www.hivemq.com)
[![Node-RED](https://img.shields.io/badge/Node--RED-Flows-8f0000?style=for-the-badge&logo=nodered&logoColor=white)](https://nodered.org)
[![Grafana](https://img.shields.io/badge/Grafana-Cloud%20Free-F46800?style=for-the-badge&logo=grafana&logoColor=white)](https://grafana.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

An intelligent, full-stack, edge-to-cloud **Autonomous IoT Operations & Predictive Maintenance Platform**. It ingests telemetry via **MQTT**, evaluates anomalies with **Scikit-Learn Machine Learning (Isolation Forest & Random Forest)**, executes **Autonomous Closed-Loop Actuations** (emergency shutdown, cooling activation, speed throttling), provides a **User-Configurable Decision Rule Engine**, orchestrates workflows with **Node-RED**, and visualizes trends on **Grafana Cloud** and **Streamlit**.

> 💡 **Designed for 100% Free 24/7 Global Hosting** on GitHub, Streamlit Community Cloud, HiveMQ Cloud Free, and Grafana Cloud Free. Accessible from any phone, tablet, or browser anywhere in the world!

---

## 🌟 Key Features

- **🎛️ Real-Time Digital Twin Dashboard:** Live telemetry monitoring for Temperature, Vibration, Hydraulic Pressure, Current, Acoustic Noise, and RPM with Plotly charts.
- **🧠 Dual-Tier Machine Learning Engine:**
  - *Unsupervised Anomaly Detection:* Scikit-Learn **Isolation Forest** detects unexpected physical deviations.
  - *Supervised Predictive Diagnosis:* **Random Forest Classifier** identifies specific failure modes: Normal, Bearing Wear, Thermal Runaway, Cavitation, Motor Overload.
  - *Equipment Health Index (0 - 100%):* Continuous asset health metric with probability scores.
- **⚙️ User-Configurable Autonomous Rule Manager:**
  - Users can toggle safety rules on/off live in the UI.
  - Edit trigger thresholds, priority levels, and actuator targets.
  - Add brand-new autonomous rules dynamically without modifying code.
  - Emergency manual override / reset button.
- **🤖 Autonomous Actuator Simulation & Closed-Loop Control:**
  - Emergency Power Breaker Trip
  - Auxiliary Cooling System Boost
  - VFD RPM Speed Throttling
  - Hydraulic Pressure Relief Valve Bypass
- **📡 Multi-Broker MQTT Client:** Connects seamlessly to **HiveMQ Cloud (TLS 8883)**, EMQX, Eclipse Mosquitto, or runs the built-in realistic physics simulator.
- **🔀 Node-RED Flow Integration:** Includes exportable `node_red_flows.json` with visual flow diagram and webhook alert triggers.
- **📈 Grafana Cloud Integration:** Includes exportable `grafana_dashboard.json` ready for 1-click import into Grafana Cloud Free tier.
- **🔔 Multi-Channel Alert Dispatch:** Automated webhook alerts (Discord, Slack, MS Teams, Zapier) and Telegram Bot notifications.

---

## 📂 Repository Structure

```
iot-autonomous-alert-platform/
├── app.py                      # Main Streamlit reactive web platform
├── ml_engine.py                # Scikit-Learn ML anomaly detection & diagnostic classifier
├── decision_engine.py          # Dynamic rule engine, debounce manager & audit logger
├── mqtt_client.py              # Paho MQTT v2 client with TLS & physics simulator
├── node_red_flows.json         # Ready-to-import Node-RED workflow configuration
├── grafana_dashboard.json      # Ready-to-import Grafana Cloud dashboard JSON model
├── test_core.py                # Automated unit & integration verification script
├── requirements.txt            # Python dependencies
├── PROJECT_SYNOPSIS.md         # Comprehensive academic & industrial project synopsis
├── .streamlit/
│   └── config.toml             # Custom dark cyber-industrial theme configuration
└── README.md                   # Setup and 24/7 free deployment instructions
```

---

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/iot-autonomous-alert-platform.git
cd iot-autonomous-alert-platform
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the verification test suite
```bash
python test_core.py
```

### 4. Launch the Streamlit Platform
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🌐 How to Deploy 24/7 Free on Streamlit Cloud & GitHub

You can publish this platform so that **anyone in the world can open it from any phone, laptop, or tablet for free**:

### Step 1: Create a GitHub Repository
1. Log into [GitHub](https://github.com) and click **New Repository**.
2. Name it `iot-autonomous-alert-platform` and make it **Public**.
3. In your local terminal, initialize and push the code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of Autonomous IoT Decision Platform"
   git branch -M main
   git remote add origin https://github.com/<your-username>/iot-autonomous-alert-platform.git
   git push -u origin main
   ```

### Step 2: Deploy to Streamlit Community Cloud (100% Free 24/7)
1. Go to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
2. Click **New app**.
3. Select your repository: `<your-username>/iot-autonomous-alert-platform`.
4. Branch: `main`.
5. Main file path: `app.py`.
6. Click **Deploy!**
7. Within 60 seconds, your application is live at `https://<your-app-name>.streamlit.app`! You can send this public URL to anyone.

---

## ☁️ 24/7 Free Cloud Infrastructure Stack

| Service | Free Tier Provider | Purpose | Link |
| :--- | :--- | :--- | :--- |
| **App Hosting** | **Streamlit Community Cloud** | Hosts the web platform 24/7 | [share.streamlit.io](https://share.streamlit.io) |
| **Code & CI/CD** | **GitHub** | Version control & auto-deployment | [github.com](https://github.com) |
| **MQTT Broker** | **HiveMQ Cloud Free** | 100 free IoT devices, TLS 8883 | [hivemq.com/cloud](https://www.hivemq.com/cloud/) |
| **Dashboards** | **Grafana Cloud Free** | 10,000 metrics, 3 dashboards 24/7 | [grafana.com](https://grafana.com) |
| **Alerts** | **Telegram Bot API / Webhooks** | Instant notifications to your phone | [telegram.org](https://telegram.org) |

---

## 🔀 Node-RED Setup Guide

1. Open your Node-RED editor (locally or hosted on Render/Railway).
2. Click the top-right menu (☰) ➡️ **Import**.
3. Copy & paste the contents of [`node_red_flows.json`](node_red_flows.json) or upload the file.
4. Click **Deploy**.
5. Node-RED will automatically subscribe to MQTT telemetry, evaluate threshold conditions, and dispatch actuator commands.

---

## 📈 Grafana Dashboard Import Guide

1. Sign up for free at [Grafana Cloud](https://grafana.com).
2. Go to **Dashboards** ➡️ **New** ➡️ **Import**.
3. Upload [`grafana_dashboard.json`](grafana_dashboard.json) or paste its JSON content.
4. Select your data source (MQTT datasource, InfluxDB, or Prometheus).
5. Click **Import** to start viewing real-time telemetry panels, gauges, and actuator status!

---

## 📱 Hardware Integration (ESP32 / Arduino / Raspberry Pi)

Any microcontroller connected to sensors can publish to this platform using standard MQTT JSON:

```cpp
// Example ESP32 Arduino snippet
#include <WiFi.h>
#include <PubSubClient.h>

const char* mqtt_broker = "broker.hivemq.com"; // Or your free HiveMQ Cloud cluster
const char* topic = "iot/telemetry/machine_01";

void sendTelemetry(float temp, float vib, float press, float curr, float acoust, float rpm) {
  char jsonBuffer[256];
  snprintf(jsonBuffer, sizeof(jsonBuffer),
    "{\"temperature\":%.2f,\"vibration\":%.2f,\"pressure\":%.2f,\"current\":%.2f,\"acoustic_noise\":%.2f,\"rpm\":%.1f}",
    temp, vib, press, curr, acoust, rpm);
  client.publish(topic, jsonBuffer);
}
```

---

## 📄 License

This project is licensed under the **MIT License** - see the LICENSE file for details.
