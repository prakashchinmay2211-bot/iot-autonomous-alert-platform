"""
AIDAMS: Autonomous IoT Decision and Alert Management System
Full-stack production Streamlit application with MQTT, Node-RED, Scikit-Learn ML, and Grafana integration.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import time

# Internal modules
from ml_engine import IoTMLEngine, FAULT_CLASSES, FEATURE_COLS
from decision_engine import AutonomousDecisionEngine, DEFAULT_RULES
from mqtt_client import MQTTHandler, IoTTelemetrySimulator

# Set Streamlit page configuration
st.set_page_config(
    page_title="AIDAMS | Autonomous IoT Decision & Alert Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark cyber-industrial IoT design
st.markdown("""
<style>
    /* Dark Theme Styling */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    .metric-card {
        background: linear-gradient(135deg, #131b2e 0%, #17223b 100%);
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    }
    .status-normal {
        color: #10b981;
        font-weight: 700;
    }
    .status-anomaly {
        color: #ef4444;
        font-weight: 700;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    .badge-critical {
        background-color: #7f1d1d;
        color: #fca5a5;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: bold;
    }
    .badge-high {
        background-color: #7c2d12;
        color: #fdba74;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: bold;
    }
    .badge-medium {
        background-color: #713f12;
        color: #fde047;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: bold;
    }
    .badge-online {
        background-color: #064e3b;
        color: #6ee7b7;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: bold;
    }
    .badge-tripped {
        background-color: #881337;
        color: #fda4af;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# State Initialization
# ---------------------------------------------------------
if "ml_engine" not in st.session_state:
    engine = IoTMLEngine()
    engine.train_models()
    st.session_state.ml_engine = engine

if "decision_engine" not in st.session_state:
    st.session_state.decision_engine = AutonomousDecisionEngine()

if "simulator" not in st.session_state:
    st.session_state.simulator = IoTTelemetrySimulator()

if "mqtt_handler" not in st.session_state:
    st.session_state.mqtt_handler = MQTTHandler()

if "history_data" not in st.session_state:
    # Initialize telemetry buffer with 30 baseline readings
    history = []
    sim = st.session_state.simulator
    for _ in range(25):
        pkt = sim.next_sample()
        ml_res = st.session_state.ml_engine.predict_telemetry(pkt)
        pkt.update({
            "is_anomaly": ml_res["is_anomaly"],
            "health_index": ml_res["health_index"],
            "predicted_fault": ml_res["predicted_fault"]
        })
        history.append(pkt)
    st.session_state.history_data = history

if "webhook_url" not in st.session_state:
    st.session_state.webhook_url = "https://httpbin.org/post"

# ---------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/processor.png", width=64)
    st.title("⚡ AIDAMS Core")
    st.caption("Autonomous IoT Decision & Alert Management")

    st.markdown("---")
    st.subheader("🛠️ Fault Injection & Simulation")
    sim_mode = st.selectbox(
        "Inject Physical Asset Condition:",
        ["Normal", "Bearing Wear", "Overheating", "Cavitation", "Overload", "Random Noise"],
        index=0
    )
    st.session_state.simulator.set_fault_mode(sim_mode)

    st.markdown("---")
    st.subheader("📡 Telemetry Stream Loop")
    auto_stream = st.toggle("Live Telemetry Streaming", value=True)
    stream_interval = st.slider("Stream Interval (sec)", 1, 5, 2)

    col_step, col_reset = st.columns(2)
    with col_step:
        step_clicked = st.button("⏩ Step Once")
    with col_reset:
        if st.button("🔄 Reset Asset"):
            st.session_state.decision_engine.reset_actuators()
            st.session_state.simulator.set_fault_mode("Normal")
            st.success("Actuators and baseline restored!")

    st.markdown("---")
    st.caption("🌐 **24/7 Cloud Architecture:**")
    st.caption("• **Engine:** Streamlit Community Cloud (Free)")
    st.caption("• **MQTT Broker:** HiveMQ Cloud (Free 100 devices)")
    st.caption("• **Telemetry Dashboards:** Grafana Cloud (Free)")
    st.caption("• **Flows:** Node-RED Engine (Importable)")

# ---------------------------------------------------------
# Telemetry Generation & Evaluation Step
# ---------------------------------------------------------
def generate_tick():
    # Produce new reading
    new_pkt = st.session_state.simulator.next_sample()
    
    # ML Prediction
    ml_res = st.session_state.ml_engine.predict_telemetry(new_pkt)
    
    # Run Autonomous Decision Engine
    executed = st.session_state.decision_engine.evaluate(
        telemetry=new_pkt,
        ml_result=ml_res,
        mqtt_client=st.session_state.mqtt_handler,
        webhook_url=st.session_state.webhook_url
    )

    # Store enriched sample
    enriched = {**new_pkt, **ml_res}
    st.session_state.history_data.append(enriched)
    if len(st.session_state.history_data) > 60:
        st.session_state.history_data.pop(0)

    # Publish to MQTT if connected
    if st.session_state.mqtt_handler.is_connected:
        st.session_state.mqtt_handler.publish("iot/telemetry/machine_01", enriched)

    return enriched, executed

# Tick if auto-stream or step clicked
if auto_stream or step_clicked:
    current_reading, recent_actions = generate_tick()
else:
    current_reading = st.session_state.history_data[-1]
    recent_actions = []

# ---------------------------------------------------------
# Main Tabs Navigation
# ---------------------------------------------------------
tab_dash, tab_rules, tab_ml, tab_nodered, tab_grafana, tab_mqtt, tab_settings = st.tabs([
    "📊 Digital Twin & Live Ops",
    "⚙️ Autonomous Rule Manager",
    "🧠 Machine Learning Studio",
    "🔀 Node-RED Workflows",
    "📈 Grafana Cloud Integration",
    "📡 MQTT Broker Connect",
    "🔔 Notifications & Alerts"
])

# =========================================================
# TAB 1: DIGITAL TWIN & LIVE OPS
# =========================================================
with tab_dash:
    # Top Status Bar
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        health_val = current_reading["health_index"]
        h_color = "#10b981" if health_val > 75 else ("#f59e0b" if health_val > 45 else "#ef4444")
        st.metric(
            label="Overall Machine Health",
            value=f"{health_val}%",
            delta=f"{round(health_val - 85, 1)}% from nominal",
            delta_color="normal" if health_val > 75 else "inverse"
        )

    with col_stat2:
        is_anom = current_reading["is_anomaly"]
        st.metric(
            label="AI Anomaly Detector",
            value="🚨 ANOMALY" if is_anom else "✅ NORMAL",
            delta=f"Risk: {current_reading['failure_risk']}%",
            delta_color="inverse" if is_anom else "normal"
        )

    with col_stat3:
        diag = current_reading["predicted_fault"]
        st.metric(
            label="Machine State Diagnosis",
            value=diag,
            delta=f"Conf: {current_reading['confidence']}%"
        )

    with col_stat4:
        pwr_state = st.session_state.decision_engine.actuator_states["power"]
        st.metric(
            label="Main Breaker Actuator",
            value=pwr_state,
            delta="Normal" if pwr_state == "ONLINE" else "TRIPPED BY AI",
            delta_color="normal" if pwr_state == "ONLINE" else "inverse"
        )

    # Anomaly Alert Banner if triggered
    if current_reading["is_anomaly"]:
        st.error(
            f"⚠️ **AUTONOMOUS ALERT ACTIVE:** Anomaly detected! Fault Mode: **{current_reading['predicted_fault']}** "
            f"(Confidence: {current_reading['confidence']}%). Top driving deviation: **{current_reading['top_driving_feature']}** "
            f"({current_reading['top_deviation_pct']:+}%). Automated countermeasures engaged."
        )

    st.markdown("### 🎛️ Live Physical Sensors")
    # Sensor cards row
    c_temp, c_vib, c_press, c_curr, c_acoust, c_rpm = st.columns(6)
    with c_temp:
        t = current_reading["temperature"]
        st.metric("Temperature", f"{t} °C", delta=f"{round(t - 62, 1)} °C", delta_color="inverse" if t > 80 else "normal")
    with c_vib:
        v = current_reading["vibration"]
        st.metric("Vibration", f"{v} mm/s", delta=f"{round(v - 1.8, 1)}", delta_color="inverse" if v > 4.5 else "normal")
    with c_press:
        p = current_reading["pressure"]
        st.metric("Hydraulic Press.", f"{p} bar", delta=f"{round(p - 4.2, 1)}", delta_color="inverse" if p > 5.5 else "normal")
    with c_curr:
        c = current_reading["current"]
        st.metric("Current Draw", f"{c} A", delta=f"{round(c - 12.5, 1)}", delta_color="inverse" if c > 18 else "normal")
    with c_acoust:
        a = current_reading["acoustic_noise"]
        st.metric("Acoustic Noise", f"{a} dB", delta=f"{round(a - 68, 1)}", delta_color="inverse" if a > 80 else "normal")
    with c_rpm:
        r = current_reading["rpm"]
        st.metric("Turbine RPM", f"{r} RPM", delta=f"{round(r - 1750, 0)}")

    # Time series graphs
    df_hist = pd.DataFrame(st.session_state.history_data)
    df_hist["step"] = range(len(df_hist))

    g_col1, g_col2 = st.columns(2)
    with g_col1:
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=df_hist["step"], y=df_hist["temperature"], mode="lines+markers", name="Temperature (°C)", line=dict(color="#f43f5e", width=2)))
        fig1.add_trace(go.Scatter(x=df_hist["step"], y=df_hist["vibration"] * 10, mode="lines+markers", name="Vibration (x10 mm/s)", line=dict(color="#38bdf8", width=2)))
        fig1.add_hline(y=85, line_dash="dash", line_color="#ef4444", annotation_text="Thermal Emergency Trip (85°C)")
        fig1.update_layout(
            title="Thermal & Vibration Telemetry (Real-Time)",
            template="plotly_dark",
            paper_bgcolor="#131b2e",
            plot_bgcolor="#0b0f19",
            margin=dict(l=20, r=20, t=40, b=20),
            height=320,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig1, use_container_width=True)

    with g_col2:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df_hist["step"], y=df_hist["pressure"] * 10, mode="lines+markers", name="Pressure (x10 bar)", line=dict(color="#a855f7", width=2)))
        fig2.add_trace(go.Scatter(x=df_hist["step"], y=df_hist["current"], mode="lines+markers", name="Current (Amperes)", line=dict(color="#facc15", width=2)))
        fig2.add_trace(go.Scatter(x=df_hist["step"], y=df_hist["health_index"], mode="lines", name="Health Index (%)", line=dict(color="#10b981", width=3, dash="dot")))
        fig2.update_layout(
            title="Hydraulic, Electrical Load & Health Index",
            template="plotly_dark",
            paper_bgcolor="#131b2e",
            plot_bgcolor="#0b0f19",
            margin=dict(l=20, r=20, t=40, b=20),
            height=320,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Actuators Status and Audit
    st.markdown("### 🤖 Autonomous Actuator & Edge Control States")
    act_col1, act_col2, act_col3, act_col4 = st.columns(4)
    act_states = st.session_state.decision_engine.actuator_states
    
    with act_col1:
        st.info(f"**Main Breaker:** `{act_states['power']}`")
    with act_col2:
        st.info(f"**Aux Cooling Pump:** `{act_states['cooling_pump']}`")
    with act_col3:
        st.info(f"**RPM Governor Limit:** `{act_states['rpm_limit']}%`")
    with act_col4:
        st.info(f"**Relief Valve:** `{act_states['relief_valve']}`")

    # Recent Audit Log
    st.markdown("### 📋 Real-Time Autonomous Decision Audit Log")
    audit_data = st.session_state.decision_engine.audit_log
    if audit_data:
        df_audit = pd.DataFrame(audit_data)
        st.dataframe(
            df_audit[["timestamp", "rule_id", "rule_name", "priority", "action", "message", "fault_diagnosis", "webhook_status"]],
            use_container_width=True,
            height=200
        )
    else:
        st.caption("No autonomous actions triggered yet. All systems nominal.")

# =========================================================
# TAB 2: AUTONOMOUS RULE MANAGER (User can make changes!)
# =========================================================
with tab_rules:
    st.header("⚙️ User-Configurable Autonomous Decision Engine")
    st.markdown("""
    Customize and control how the autonomous IoT system responds to anomalies.
    You can toggle existing safety rules, tweak trigger thresholds, or create brand-new autonomous rules.
    """)

    dec_engine = st.session_state.decision_engine

    # Display Current Rules with editable toggles
    st.subheader("Active Autonomous Rules")
    for idx, rule in enumerate(dec_engine.rules):
        with st.expander(f"🔹 [{rule['priority']}] {rule['id']}: {rule['name']}", expanded=(idx == 0)):
            c_r1, c_r2, c_r3 = st.columns([1, 2, 1])
            with c_r1:
                enabled = st.checkbox("Enabled", value=rule["enabled"], key=f"rule_en_{rule['id']}")
                rule["enabled"] = enabled
            with c_r2:
                st.write(f"**Action Triggered:** `{rule['action']}` on `{rule.get('action_param', 'system')}`")
                st.write(f"**Message:** {rule['message']}")
                st.write(f"**Cooldown Debounce:** {rule.get('cooldown_seconds', 30)}s")
            with c_r3:
                st.json(rule["conditions"])
                if st.button("🗑️ Delete Rule", key=f"del_rule_{rule['id']}"):
                    dec_engine.delete_rule(rule["id"])
                    st.rerun()

    st.markdown("---")
    st.subheader("➕ Create New Autonomous Decision Rule")
    with st.form("new_rule_form"):
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            new_id = st.text_input("Rule ID", value=f"RULE_{len(dec_engine.rules) + 1:02d}")
            new_name = st.text_input("Rule Name", value="Bearing Overheat Auto-Governor")
            new_priority = st.selectbox("Priority Level", ["CRITICAL", "HIGH", "MEDIUM", "LOW", "WARNING"])
            new_action = st.selectbox("Autonomous Action", [
                "EMERGENCY_SHUTDOWN", "ACTIVATE_COOLING", "THROTTLE_MOTOR", "PRESSURE_RELIEF", "DISPATCH_ALERT"
            ])
            new_action_param = st.text_input("Actuator Target / MQTT Topic", value="asset/motor_01/control")
        with f_col2:
            st.write("**Trigger Conditions:**")
            cond_temp = st.number_input("Trigger if Temperature > (°C)", min_value=0.0, max_value=200.0, value=82.0)
            cond_vib = st.number_input("Trigger if Vibration > (mm/s)", min_value=0.0, max_value=20.0, value=5.0)
            cond_health = st.number_input("Trigger if Health Index < (%)", min_value=0.0, max_value=100.0, value=50.0)
            cond_ml_anom = st.checkbox("Require Machine Learning Anomaly Flag", value=True)
            new_msg = st.text_area("Alert & Action Message", value="Automated intervention executed due to combined temperature and vibration threshold violation.")
            cooldown = st.number_input("Cooldown Period (seconds)", min_value=5, max_value=300, value=30)

        submitted = st.form_submit_button("💾 Save & Activate Rule")
        if submitted:
            new_rule_dict = {
                "id": new_id,
                "name": new_name,
                "enabled": True,
                "priority": new_priority,
                "conditions": {
                    "temperature_gt": cond_temp,
                    "vibration_gt": cond_vib,
                    "health_index_lt": cond_health,
                    "require_ml_anomaly": cond_ml_anom
                },
                "action": new_action,
                "action_param": new_action_param,
                "message": new_msg,
                "cooldown_seconds": cooldown
            }
            dec_engine.add_rule(new_rule_dict)
            st.success(f"Rule {new_id} successfully created and integrated into the real-time evaluation loop!")
            st.rerun()

# =========================================================
# TAB 3: MACHINE LEARNING STUDIO
# =========================================================
with tab_ml:
    st.header("🧠 Machine Learning Studio & Predictive Maintenance")
    st.markdown("""
    The system employs a dual-tier ML architecture:
    1. **Isolation Forest (Unsupervised):** Continuous anomaly score detection on unseen patterns.
    2. **Random Forest Classifier (Supervised):** Diagnoses specific failure modes with confidence probabilities.
    """)

    ml_col1, ml_col2 = st.columns([1, 1])

    with ml_col1:
        st.subheader("Model Configuration & Live Retraining")
        retrain_contamination = st.slider("Anomaly Contamination Rate", 0.05, 0.30, 0.15, step=0.01)
        retrain_estimators = st.slider("Number of Decision Trees", 50, 200, 100, step=10)
        
        if st.button("🚀 Retrain ML Pipeline"):
            with st.spinner("Generating synthetic industrial telemetry and retraining models..."):
                metrics = st.session_state.ml_engine.train_models(
                    contamination=retrain_contamination,
                    n_estimators=retrain_estimators
                )
                st.success(f"Models retrained! Classification Accuracy: **{metrics['accuracy']}%** across {metrics['samples_trained']} samples.")

        st.markdown("#### Model Performance Metrics")
        m = st.session_state.ml_engine.metrics
        st.write(f"• **Supervised Diagnostic Accuracy:** `{m.get('accuracy', 98.4)}%`")
        st.write(f"• **Contamination Rate:** `{m.get('contamination', 0.15)}`")
        st.write(f"• **Tree Estimators:** `{m.get('n_estimators', 100)}`")
        st.write(f"• **Training Samples:** `{m.get('samples_trained', 2500)}`")

    with ml_col2:
        st.subheader("Feature Importance Distribution")
        importances = st.session_state.ml_engine.metrics.get("feature_importances", {
            "temperature": 0.28, "vibration": 0.25, "pressure": 0.18, "current": 0.15, "acoustic_noise": 0.10, "rpm": 0.04
        })
        df_feat = pd.DataFrame({
            "Feature": list(importances.keys()),
            "Importance": list(importances.values())
        }).sort_values("Importance", ascending=True)

        fig_feat = px.bar(
            df_feat, x="Importance", y="Feature", orientation="h",
            color="Importance", color_continuous_scale="Viridis",
            title="Sensor Feature Weights in Fault Diagnosis"
        )
        fig_feat.update_layout(
            template="plotly_dark",
            paper_bgcolor="#131b2e",
            plot_bgcolor="#0b0f19",
            margin=dict(l=20, r=20, t=40, b=20),
            height=280
        )
        st.plotly_chart(fig_feat, use_container_width=True)

    # Class Probabilities Radar / Bar Chart for current sample
    st.subheader("Current Telemetry Diagnosis Breakdown")
    prob_dict = current_reading.get("class_probabilities", {})
    if prob_dict:
        df_probs = pd.DataFrame({
            "Operational State": list(prob_dict.keys()),
            "Probability (%)": list(prob_dict.values())
        })
        fig_p = px.bar(
            df_probs, x="Operational State", y="Probability (%)",
            color="Probability (%)", color_continuous_scale="Reds",
            title=f"Predicted State Probabilities (Top: {current_reading['predicted_fault']} at {current_reading['confidence']}%)"
        )
        fig_p.update_layout(
            template="plotly_dark",
            paper_bgcolor="#131b2e",
            plot_bgcolor="#0b0f19",
            margin=dict(l=20, r=20, t=40, b=20),
            height=300
        )
        st.plotly_chart(fig_p, use_container_width=True)

# =========================================================
# TAB 4: NODE-RED WORKFLOWS
# =========================================================
with tab_nodered:
    st.header("🔀 Node-RED Orchestration & Flow Automation")
    st.markdown("""
    Node-RED provides edge-to-cloud visual wiring for the platform.
    Below is the complete architectural flow diagram and exportable JSON flow ready for one-click import into Node-RED.
    """)

    # Visual Flow diagram using Mermaid representation
    st.subheader("Flow Architecture Diagram")
    st.markdown("""
    ```mermaid
    flowchart LR
        A[MQTT In: iot/telemetry] --> B[Function: Threshold & ML Evaluation]
        B --> C{Action Needed?}
        C -->|Yes: Thermal Runaway| D[Actuator: Force Cooling Pump 100%]
        C -->|Yes: Bearing Spike| E[Actuator: Throttle RPM 50%]
        C -->|Yes: Emergency| F[Actuator: Trip Power Breaker]
        C -->|Yes: Dispatch| G[HTTP / Telegram Alert]
        C -->|No: Nominal| H[Grafana / InfluxDB Push]
    ```
    """)

    # Download Node-RED Flow
    try:
        with open("node_red_flows.json", "r") as f:
            flow_content = f.read()
    except Exception:
        flow_content = "[]"

    st.download_button(
        label="📥 Download node_red_flows.json",
        data=flow_content,
        file_name="node_red_flows.json",
        mime="application/json"
    )

    with st.expander("👁️ View Complete Node-RED Flow JSON"):
        st.code(flow_content, language="json")

    st.markdown("""
    #### 🚀 How to Run in Node-RED:
    1. Open your Node-RED dashboard (`http://localhost:1880` or hosted cloud instance).
    2. Click the hamburger menu (top right) ➡️ **Import**.
    3. Paste the contents of `node_red_flows.json` or upload the file.
    4. Click **Deploy**. Node-RED will immediately start listening to `iot/telemetry/machine_01` and executing autonomous actions.
    """)

# =========================================================
# TAB 5: GRAFANA CLOUD INTEGRATION
# =========================================================
with tab_grafana:
    st.header("📈 Grafana Cloud Live Telemetry Dashboards")
    st.markdown("""
    Export telemetry seamlessly into **Grafana Cloud Free Tier (100% Free 24/7)**.
    The dashboard includes equipment health gauges, multi-sensor time-series graphs, and autonomous breaker state indicators.
    """)

    try:
        with open("grafana_dashboard.json", "r") as f:
            grafana_json = f.read()
    except Exception:
        grafana_json = "{}"

    st.download_button(
        label="📥 Download grafana_dashboard.json (Ready to Import)",
        data=grafana_json,
        file_name="grafana_dashboard.json",
        mime="application/json"
    )

    st.subheader("Grafana Dashboard Mockup & Preview")
    # Interactive Grafana styled preview
    g_m1, g_m2, g_m3, g_m4 = st.columns(4)
    with g_m1:
        st.markdown("""
        <div class="metric-card">
            <span style="color:#94a3b8; font-size:12px;">GRAFANA GAUGE</span>
            <h2 style="color:#00f2fe; margin:5px 0;">Health: """ + str(current_reading['health_index']) + """%</h2>
            <div style="background:#1e293b; border-radius:5px; height:8px; overflow:hidden;">
                <div style="background:#00f2fe; width:""" + str(current_reading['health_index']) + """%; height:100%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with g_m2:
        st.markdown("""
        <div class="metric-card">
            <span style="color:#94a3b8; font-size:12px;">GRAFANA STAT</span>
            <h2 style="color:""" + ("#ef4444" if current_reading['is_anomaly'] else "#10b981") + """; margin:5px 0;">""" + ("ANOMALY" if current_reading['is_anomaly'] else "NOMINAL") + """</h2>
            <span style="color:#94a3b8; font-size:12px;">AI Model: IsolationForest</span>
        </div>
        """, unsafe_allow_html=True)
    with g_m3:
        st.markdown("""
        <div class="metric-card">
            <span style="color:#94a3b8; font-size:12px;">ACTUATOR STATUS</span>
            <h2 style="color:#f59e0b; margin:5px 0;">""" + str(st.session_state.decision_engine.actuator_states['cooling_pump']) + """</h2>
            <span style="color:#94a3b8; font-size:12px;">Auxiliary Cooling</span>
        </div>
        """, unsafe_allow_html=True)
    with g_m4:
        st.markdown("""
        <div class="metric-card">
            <span style="color:#94a3b8; font-size:12px;">MAIN BREAKER</span>
            <h2 style="color:""" + ("#10b981" if st.session_state.decision_engine.actuator_states['power'] == 'ONLINE' else "#ef4444") + """; margin:5px 0;">""" + str(st.session_state.decision_engine.actuator_states['power']) + """</h2>
            <span style="color:#94a3b8; font-size:12px;">Emergency Interlock</span>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("👁️ View Full Grafana JSON Model"):
        st.code(grafana_json, language="json")

    st.markdown("""
    #### 🛠️ Step-by-Step 24/7 Free Grafana Cloud Setup:
    1. Sign up for a free forever account at [grafana.com](https://grafana.com) (includes 10,000 metrics, 3 dashboards, 24/7).
    2. Go to **Dashboards** ➡️ **New** ➡️ **Import**.
    3. Paste the contents of `grafana_dashboard.json` or upload the file.
    4. Select your data source (MQTT Plugin, InfluxDB, or Prometheus).
    5. Save! You now have a real-time 24/7 Grafana monitoring dashboard accessible from any browser or smartphone.
    """)

# =========================================================
# TAB 6: MQTT BROKER CONNECT
# =========================================================
with tab_mqtt:
    st.header("📡 Live MQTT Broker Connectivity")
    st.markdown("""
    Connect directly to **HiveMQ Cloud Free (24/7 Free Cluster)**, EMQX, Eclipse Mosquitto, or AWS IoT Core.
    """)

    m_col1, m_col2 = st.columns([1, 1])

    with m_col1:
        st.subheader("Broker Connection Settings")
        mqtt_host = st.text_input("MQTT Broker Host", value="broker.hivemq.com")
        mqtt_port = st.number_input("Port (1883 for TCP, 8883 for TLS)", value=1883)
        mqtt_user = st.text_input("Username (Optional)", value="")
        mqtt_pass = st.text_input("Password (Optional)", type="password", value="")
        use_tls = st.checkbox("Enable TLS/SSL (Required for 8883)", value=False)

        c_conn, c_disconn = st.columns(2)
        with c_conn:
            if st.button("🔌 Connect to Broker"):
                handler = MQTTHandler(
                    broker=mqtt_host,
                    port=int(mqtt_port),
                    username=mqtt_user if mqtt_user else None,
                    password=mqtt_pass if mqtt_pass else None,
                    use_tls=use_tls
                )
                success, msg = handler.connect()
                st.session_state.mqtt_handler = handler
                if success:
                    st.success(f"Connected to {mqtt_host}:{mqtt_port}!")
                else:
                    st.error(msg)
        with c_disconn:
            if st.button("❌ Disconnect"):
                st.session_state.mqtt_handler.disconnect()
                st.info("MQTT client disconnected.")

        is_conn = st.session_state.mqtt_handler.is_connected
        st.write(f"**Connection Status:** {'🟢 CONNECTED' if is_conn else '🔴 DISCONNECTED (Using Built-in Telemetry Engine)'}")

    with m_col2:
        st.subheader("Manual MQTT Publisher & Tester")
        pub_topic = st.text_input("Publish Topic", value="iot/actuator/manual_override")
        pub_payload = st.text_area("Payload JSON", value='{\n  "command": "TRIGGER_TEST",\n  "severity": "INFO"\n}')
        if st.button("📤 Publish MQTT Message"):
            if st.session_state.mqtt_handler.is_connected:
                st.session_state.mqtt_handler.publish(pub_topic, pub_payload)
                st.success(f"Published to `{pub_topic}`!")
            else:
                st.warning("Connect to an MQTT broker first or use the built-in simulator.")

        st.subheader("Incoming MQTT Feed Buffer")
        in_msgs = list(st.session_state.mqtt_handler.incoming_queue)
        if in_msgs:
            st.json(in_msgs[-5:])
        else:
            st.caption("No incoming MQTT messages yet on subscribed topics.")

# =========================================================
# TAB 7: NOTIFICATIONS & SETTINGS
# =========================================================
with tab_settings:
    st.header("🔔 Automated Notification Dispatch & Webhooks")
    st.markdown("""
    Configure webhook endpoints (Discord, Slack, Microsoft Teams, Node-RED, Telegram) 
    that the autonomous decision engine calls when critical events occur.
    """)

    st.subheader("Webhook Integration")
    webhook_val = st.text_input("Alert Webhook URL (POST)", value=st.session_state.webhook_url)
    st.session_state.webhook_url = webhook_val

    if st.button("🧪 Send Test Alert Webhook"):
        test_payload = {
            "event": "MANUAL_TEST_ALERT",
            "message": "Testing AIDAMS autonomous notification pipeline.",
            "timestamp": datetime.now().isoformat(),
            "status": "OPERATIONAL"
        }
        try:
            res = requests.post(webhook_val, json=test_payload, timeout=3.0)
            st.success(f"Webhook test dispatched successfully! Response code: {res.status_code}")
        except Exception as e:
            st.error(f"Webhook dispatch failed: {str(e)}")

    st.markdown("---")
    st.subheader("Telegram Bot Integration")
    st.text_input("Telegram Bot Token", value="", placeholder="e.g., 123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ")
    st.text_input("Telegram Chat / Channel ID", value="", placeholder="e.g., -100123456789")
    st.caption("When configured, critical emergency cutoff and anomaly events will be automatically forwarded to your phone.")

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; font-size: 13px;'>"
    "⚡ <b>AIDAMS: Autonomous IoT Decision and Alert Management Platform</b> | "
    "Designed for 24/7 Free Cloud Deployment via GitHub & Streamlit Community Cloud"
    "</div>",
    unsafe_allow_html=True
)

# Auto-refresh loop when streaming is enabled
if auto_stream:
    time.sleep(stream_interval)
    st.rerun()
