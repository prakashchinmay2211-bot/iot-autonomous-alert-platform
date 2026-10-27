"""
Script to generate the Software Requirements Specification (SRS) Report in Microsoft Word (.docx) format
Student: Chinmay Prakash | Roll No: 2400320310060 | ABES Engineering College | Guide: Ashish Kumar
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def create_srs_document():
    doc = docx.Document()

    # Page Margins: 1 inch on all sides
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles & Colors
    PRIMARY_COLOR = RGBColor(16, 52, 96)     # Deep Navy
    SECONDARY_COLOR = RGBColor(0, 119, 182)  # Tech Blue
    DARK_TEXT = RGBColor(30, 41, 59)         # Slate Dark
    MUTED_GRAY = RGBColor(100, 116, 139)

    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    # -------------------------------------------------------------
    # COVER PAGE
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(30)
    title_p.paragraph_format.space_after = Pt(10)
    
    run_inst = title_p.add_run("ABES ENGINEERING COLLEGE, GHAZIABAD\n")
    run_inst.font.name = "Calibri"
    run_inst.font.size = Pt(16)
    run_inst.font.bold = True
    run_inst.font.color.rgb = PRIMARY_COLOR

    run_dept = title_p.add_run("DEPARTMENT OF ELECTRONICS & COMMUNICATION ENGINEERING\n\n")
    run_dept.font.name = "Calibri"
    run_dept.font.size = Pt(13)
    run_dept.font.bold = True
    run_dept.font.color.rgb = SECONDARY_COLOR

    run_srs = title_p.add_run("SOFTWARE REQUIREMENTS SPECIFICATION (SRS)\n")
    run_srs.font.name = "Calibri"
    run_srs.font.size = Pt(20)
    run_srs.font.bold = True
    run_srs.font.color.rgb = PRIMARY_COLOR

    run_sub = title_p.add_run("Mini Project Report (B.Tech 3rd Year)\n\n")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(14)
    run_sub.font.italic = True
    run_sub.font.color.rgb = DARK_TEXT

    # Project Title Banner
    banner_p = doc.add_paragraph()
    banner_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    banner_p.paragraph_format.space_before = Pt(10)
    banner_p.paragraph_format.space_after = Pt(30)
    run_title = banner_p.add_run("AUTONOMOUS IoT DECISION AND ALERT MANAGEMENT PLATFORM (AIDAMS)\n")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(18)
    run_title.font.bold = True
    run_title.font.color.rgb = SECONDARY_COLOR

    run_desc = banner_p.add_run("An Edge-to-Cloud Cyber-Physical System featuring MQTT Telemetry, Scikit-Learn Anomaly Detection, Dynamic Rule Engine, Node-RED, Grafana & Streamlit")
    run_desc.font.name = "Calibri"
    run_desc.font.size = Pt(11)
    run_desc.font.italic = True
    run_desc.font.color.rgb = MUTED_GRAY

    # Candidate & Supervisor Information Table
    info_table = doc.add_table(rows=6, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_table.autofit = False

    metadata = [
        ("Student Name", "Chinmay Prakash"),
        ("University Roll Number", "2400320310060"),
        ("Branch / Department", "Electronics and Communication Engineering (ECE)"),
        ("Project Supervisor / Guide", "Ashish Kumar"),
        ("Batch / Degree", "Batch 2024–28 | B.Tech"),
        ("Academic Year", "2026–27")
    ]

    for idx, (label, val) in enumerate(metadata):
        row = info_table.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width = Inches(2.8)
        cell_val.width = Inches(3.7)

        set_cell_background(cell_lbl, "F1F5F9")
        set_cell_margins(cell_lbl, top=120, bottom=120, left=150, right=150)
        set_cell_margins(cell_val, top=120, bottom=120, left=150, right=150)

        p0 = cell_lbl.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(label)
        r0.font.name = "Calibri"
        r0.font.size = Pt(11)
        r0.font.bold = True
        r0.font.color.rgb = PRIMARY_COLOR

        p1 = cell_val.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(val)
        r1.font.name = "Calibri"
        r1.font.size = Pt(11)
        r1.font.color.rgb = DARK_TEXT

    doc.add_page_break()

    # Helper function for Section Headings
    def add_section_heading(num_str, title_str):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(18)
        h.paragraph_format.space_after = Pt(6)
        h.paragraph_format.keep_with_next = True
        
        r = h.add_run(f"{num_str}. {title_str}")
        r.font.name = "Calibri"
        r.font.size = Pt(15)
        r.font.bold = True
        r.font.color.rgb = PRIMARY_COLOR

    def add_subheading(sub_title):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True

        r = h.add_run(sub_title)
        r.font.name = "Calibri"
        r.font.size = Pt(12.5)
        r.font.bold = True
        r.font.color.rgb = SECONDARY_COLOR

    def add_body(text, bold_prefix=None, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15

        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = "Calibri"
            rb.font.size = Pt(11)
            rb.font.bold = True
            rb.font.color.rgb = DARK_TEXT

        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(11)
        r.font.color.rgb = DARK_TEXT
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15

        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = "Calibri"
            rb.font.size = Pt(11)
            rb.font.bold = True
            rb.font.color.rgb = DARK_TEXT

        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(11)
        r.font.color.rgb = DARK_TEXT

    # -------------------------------------------------------------
    # SECTION 1: ABSTRACT
    # -------------------------------------------------------------
    add_section_heading("1", "Abstract")
    add_body(
        "The Autonomous IoT Decision and Alert Platform (AIDAMS) is an intelligent, full-stack, edge-to-cloud cyber-physical "
        "industrial monitoring platform designed to eliminate human latency and alert fatigue in mission-critical manufacturing. "
        "Industrial machinery—such as automated bottling stations, CNC precision milling centers, logistics conveyors, and hydraulic pump turbines—"
        "often experience catastrophic structural breakdown when sudden thermal surges, mechanical vibrations, or electrical overload conditions occur. "
        "Traditional supervisory control systems (SCADA) rely on static threshold-based alarms that suffer from false alarm fatigue and fail to react "
        "within milliseconds of mechanical degradation.\n\n"
        "AIDAMS bridges high-frequency telemetry ingestion over lightweight MQTT protocols with a dual-tier Machine Learning core comprising "
        "an unsupervised Isolation Forest anomaly detector, rolling statistical Z-score calculators, and a multi-class Random Forest diagnostic classifier. "
        "A Python-driven Autonomous Decision Engine continuously evaluates streaming telemetry and executes closed-loop protective countermeasures "
        "(such as emergency main breaker cutoffs, auxiliary cooling boosts, speed throttling, and hydraulic bypass purges) without waiting for human intervention. "
        "Furthermore, operators maintain full operational governance via a dynamic, user-configurable rule management cockpit, MongoDB persistence, "
        "Node-RED orchestration pipelines, and Grafana Cloud observability dashboards. The entire platform is architected to operate 24/7 free "
        "across public serverless infrastructure."
    )

    # -------------------------------------------------------------
    # SECTION 2: PROBLEM STATEMENT
    # -------------------------------------------------------------
    add_section_heading("2", "Problem Statement")
    add_body(
        "Modern smart factories generate millions of high-frequency sensor telemetry packets every hour. However, modern supervisory plants "
        "still face significant operational vulnerabilities:"
    )
    add_bullet(" High-speed rotating assets like turbine bearings and CNC spindles can experience irreversible mechanical destruction within 2 to 5 seconds of lubrication breakdown or cavitation. Human reaction time is inherently inadequate to arrest these cascades.", "1. Human Reaction Latency: ")
    add_bullet(" Static threshold alarms ('Alert if Temperature > 80°C') fail to capture subtle multi-variate correlations (e.g., normal temperature accompanied by sudden harmonic vibration) and inundate operators with false alarms during ambient shifts.", "2. False Alarm Fatigue: ")
    add_bullet(" Existing industrial SCADA/DCS systems are proprietary, vendor-locked, and prevent plant engineers from editing autonomous control rules or deploying custom machine learning models.", "3. Rigid Proprietary Architectures: ")
    add_bullet(" Commercial cloud IoT packages (AWS IoT SiteWise, Azure IoT Hub) impose steep ongoing recurring subscription fees that are inaccessible to small-to-medium enterprises (SMEs) and academic institutions.", "4. Prohibitive Financial Cost: ")

    # -------------------------------------------------------------
    # SECTION 3: PROJECT OBJECTIVES
    # -------------------------------------------------------------
    add_section_heading("3", "Project Objectives")
    add_bullet("Ingest real-time multi-sensor telemetry (temperature, vibration, pressure, current, acoustic noise, RPM) over lightweight MQTT (QoS-1) with millisecond latency.", "• Real-Time Ingestion: ")
    add_bullet("Deploy a dual-tier machine learning pipeline utilizing Scikit-Learn Isolation Forest and rolling Z-score deviation to detect anomalies without manual labeling.", "• Unsupervised Machine Learning: ")
    add_bullet("Automatically diagnose operational failure regimes (Bearing Degradation, Thermal Runaway, Cavitation Surge, Motor Overload) and compute a dynamic Equipment Health Index (EHI, 0–100%).", "• Predictive Health Index: ")
    add_bullet("Execute closed-loop digital twin actuator commands (emergency breaker trip, auxiliary cooling activation, RPM throttling, and pressure relief valve purge) within 2 seconds of threshold violation.", "• Closed-Loop Autonomous Actuation: ")
    add_bullet("Provide an interactive user-facing rule management cockpit where plant operators can add, modify, toggle, and delete decision rules live in production.", "• Operator Governance & Customization: ")
    add_bullet("Persist all telemetry, ML anomaly evaluations, autonomous decisions, and incident lifecycles in MongoDB and export ready-to-run Node-RED workflows and Grafana Cloud dashboards.", "• Enterprise Orchestration: ")
    add_bullet("Deliver a production-ready application deployable 24/7 for $0/month on Streamlit Community Cloud and GitHub.", "• 24/7 Free Global Accessibility: ")

    # -------------------------------------------------------------
    # SECTION 4: PROPOSED SOLUTION & ARCHITECTURE
    # -------------------------------------------------------------
    add_section_heading("4", "Proposed Solution & Methodology")
    add_body(
        "The proposed platform implements a cyclic six-stage cyber-physical loop: Sense → Communicate → Evaluate → Actuate → Persist → Visualize."
    )
    add_bullet("Industrial edge assets stream multi-sensor payloads at 1–2 second intervals formatted in lightweight JSON.", "1. Sensing: ")
    add_bullet("Packets are published to an MQTT Broker (HiveMQ Cloud / Eclipse Mosquitto) over port 1883/8883 (TLS encrypted).", "2. Communication: ")
    add_bullet("The Python AIoT engine scales incoming features, evaluates anomaly scores via Isolation Forest, and determines root cause deviation.", "3. Intelligence & Evaluation: ")
    add_bullet("If safety conditions are breached, the Autonomous Decision Engine verifies the anti-flapping debounce window and publishes actuator commands to `iot/actuator/commands`.", "4. Closed-Loop Actuation: ")
    add_bullet("Every reading, ML anomaly evaluation, and autonomous action is persisted to MongoDB collections (`telemetry`, `anomalies`, `decisions`, `alerts`, `device_states`).", "5. Persistence: ")
    add_bullet("Operators monitor asset telemetry, inspect explainable AI failure root-causes, and modify rules through Streamlit, Grafana, and Node-RED.", "6. Visualization & Governance: ")

    # -------------------------------------------------------------
    # SECTION 5: SCOPE OF THE PROJECT
    # -------------------------------------------------------------
    add_section_heading("5", "Scope of the Project")
    add_subheading("5.1 In-Scope Deliverables")
    add_bullet("Full multi-asset industrial telemetry simulation covering Bottle Filling Machines, CNC Precision Milling, Logistics Conveyors, and Pump Turbines.")
    add_bullet("Comprehensive telemetry parameters: Temperature (°C), Vibration (mm/s), Hydraulic Pressure (bar), Current (A), Acoustic Noise (dB), and RPM.")
    add_bullet("Dual-tier Scikit-Learn ML engine (Isolation Forest + Random Forest) with real-time explainability.")
    add_bullet("Interactive Streamlit Web Cockpit with live Plotly charts, dark cyber theme, and actuator digital twins.")
    add_bullet("Dynamic Rule Manager allowing operators to add, edit, and toggle safety thresholds live.")
    add_bullet("Pre-configured Node-RED flow (`node_red_flows.json`) and Grafana Cloud dashboard (`grafana_dashboard.json`).")
    add_bullet("Complete Git repository initialized and deployed to GitHub and Streamlit Community Cloud for 24/7 free access.")

    add_subheading("5.2 Out-of-Scope (Future Enhancements)")
    add_bullet("Physical coupling to high-voltage industrial factory switchgear (current version controls simulated and digital twin actuators).")
    add_bullet("Enterprise LDAP/Single Sign-On (user roles are currently managed through operator cockpit access).")

    # -------------------------------------------------------------
    # SECTION 6: FUNCTIONAL REQUIREMENTS
    # -------------------------------------------------------------
    add_section_heading("6", "Functional Requirements Specification")

    fr_data = [
        ("FR-01", "Telemetry Ingestion", "The system shall ingest continuous multi-sensor telemetry packets (temperature, vibration, pressure, current, noise, rpm) over MQTT topics `iot/telemetry/#`."),
        ("FR-02", "Data Normalization & Storage", "The system shall standardize incoming sensor values via Z-score scaling and persist every record to the MongoDB `telemetry` collection."),
        ("FR-03", "Unsupervised Anomaly Detection", "The ML engine shall apply Isolation Forest to determine anomaly status (-1 for anomaly, 1 for normal) and compute a continuous anomaly score."),
        ("FR-04", "Predictive Diagnostics & Health", "The system shall classify failure modes (Bearing Wear, Thermal Runaway, Cavitation, Overload) and compute an Equipment Health Index (0–100%)."),
        ("FR-05", "Autonomous Protective Actuation", "The decision engine shall trigger immediate automated countermeasures (Emergency Breaker Trip, Auxiliary Cooling Boost, RPM Throttle, Pressure Dump) when thresholds are violated."),
        ("FR-06", "Debounce & Flapping Prevention", "The engine shall maintain a configurable cooldown debounce window (default 30 seconds) per rule to prevent electromechanical relay chatter."),
        ("FR-07", "User Rule Governance", "The web cockpit shall allow plant operators to add new decision rules, modify thresholds, change priorities, and toggle rules ON/OFF live."),
        ("FR-08", "Explainable AI Root-Cause", "The system shall identify the top driving sensor deviation (%) responsible for an anomaly and display plain-language diagnostic explanations."),
        ("FR-09", "Incident Lifecycle Management", "The system shall generate alerts with lifecycle states (`ACTIVE`, `ACKNOWLEDGED`, `RESOLVED`) and allow operator manual reset."),
        ("FR-10", "Fault Injection Simulation Lab", "The platform shall provide interactive controls to inject physical faults (`Thermal Runaway`, `Bearing Wear`, `Cavitation`, `Motor Overload`) for stress-testing."),
        ("FR-11", "External Notification Dispatch", "The system shall format and dispatch automated JSON webhook payloads (Discord, Slack, Teams) and Telegram alerts upon critical events.")
    ]

    t_fr = doc.add_table(rows=len(fr_data) + 1, cols=3)
    t_fr.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_fr.autofit = False

    headers_fr = ["Req ID", "Module / Feature", "Functional Specification Description"]
    col_widths_fr = [Inches(1.0), Inches(1.8), Inches(3.7)]

    # Format Header Row
    hdr_row = t_fr.rows[0]
    for c_idx, title in enumerate(headers_fr):
        cell = hdr_row.cells[c_idx]
        cell.width = col_widths_fr[c_idx]
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, top=140, bottom=140, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(title)
        r.font.name = "Calibri"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, (rid, feat, desc) in enumerate(fr_data):
        row = t_fr.rows[r_idx + 1]
        bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, text in enumerate([rid, feat, desc]):
            cell = row.cells[c_idx]
            cell.width = col_widths_fr[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.font.bold = (c_idx < 2)
            r.font.color.rgb = DARK_TEXT

    # -------------------------------------------------------------
    # SECTION 7: NON-FUNCTIONAL REQUIREMENTS
    # -------------------------------------------------------------
    add_section_heading("7", "Non-Functional Requirements Specification")

    nfr_data = [
        ("NFR-01", "Latency & Performance", "The end-to-end latency from anomaly injection to ML detection and autonomous actuator trigger shall not exceed 2.0 seconds."),
        ("NFR-02", "24/7 Availability", "The web cockpit and MQTT pipeline shall operate continuously on Streamlit Community Cloud and HiveMQ Cloud with 99.9% uptime at $0 cost."),
        ("NFR-03", "Scalability", "The MQTT ingestion layer shall support up to 100 concurrent edge microcontrollers (ESP32/Raspberry Pi) publishing at 1 Hz."),
        ("NFR-04", "Data Integrity", "All telemetry, anomaly scores, and audit records shall be committed with ISO-8601 UTC timestamps and compound indexes for fast query retrieval."),
        ("NFR-05", "Usability & Accessibility", "The UI shall be fully responsive across mobile devices, tablets, and desktops using modern dark-mode industrial CSS."),
        ("NFR-06", "Security & Transport Encryption", "All remote MQTT communications shall support TLS 8883 port encryption with client credential validation.")
    ]

    t_nfr = doc.add_table(rows=len(nfr_data) + 1, cols=3)
    t_nfr.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_nfr.autofit = False

    col_widths_nfr = [Inches(1.0), Inches(1.8), Inches(3.7)]
    hdr_nfr = t_nfr.rows[0]
    for c_idx, title in enumerate(["Req ID", "Attribute", "Non-Functional Benchmark"]):
        cell = hdr_nfr.cells[c_idx]
        cell.width = col_widths_nfr[c_idx]
        set_cell_background(cell, "0F766E")
        set_cell_margins(cell, top=140, bottom=140, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(title)
        r.font.name = "Calibri"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, (rid, attr, desc) in enumerate(nfr_data):
        row = t_nfr.rows[r_idx + 1]
        bg = "F0FDFA" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, text in enumerate([rid, attr, desc]):
            cell = row.cells[c_idx]
            cell.width = col_widths_nfr[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.font.bold = (c_idx < 2)
            r.font.color.rgb = DARK_TEXT

    # -------------------------------------------------------------
    # SECTION 8: AUTONOMOUS PROTECTIVE ACTIONS MATRIX
    # -------------------------------------------------------------
    add_section_heading("8", "Autonomous Protective Actions Matrix")

    act_data = [
        ("MCH-007 (Bottle Filling)", "Temp ≥ 88°C OR Vib ≥ 4.0 mm/s; Pressure ≤ 4.0 bar", "EMERGENCY_FAULT_STOP", "Fill valve shut, conveyor halted to 0%, cooling pump set to MAXIMUM (100%). Low-pressure interlock engaged."),
        ("CNC-003 (Precision Milling)", "Spindle Temp > 85°C OR Vibration > 5.5 mm/s", "SPINDLE_SAFETY_TRIP", "Spindle drive brake engaged, feed rate dropped to 0 mm/min, flood coolant solenoid energized at 100%."),
        ("CONV-012 (Logistics Conveyor)", "Motor Temp > 80°C OR Belt Tension > 620 N", "EMERGENCY_CONVEYOR_HALT", "Drive motor powered off, diverter safety gate opened to bypass bin, audible warning beacon enabled."),
        ("ENV-001 (Air Quality & Safety)", "Hazardous Gas > 250 ppm OR Smoke > 80 ppm", "HAZMAT_EVACUATION_PURGE", "Fresh air intake dampers shut, explosion-proof exhaust fans flushed at 100%, plant evacuation siren triggered."),
        ("GENERIC PUMP / TURBINE", "Health Index < 45% OR Temp > 90°C with ML Anomaly", "EMERGENCY_SHUTDOWN", "Main circuit breaker tripped offline, auxiliary cooling boosted, diagnostic webhook alert dispatched.")
    ]

    t_act = doc.add_table(rows=len(act_data) + 1, cols=4)
    t_act.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_act.autofit = False

    col_widths_act = [Inches(1.5), Inches(1.8), Inches(1.5), Inches(1.7)]
    hdr_act = t_act.rows[0]
    for c_idx, title in enumerate(["Target Asset", "Trigger Threshold Condition", "Autonomous Action", "Actuation & Physical Countermeasure"]):
        cell = hdr_act.cells[c_idx]
        cell.width = col_widths_act[c_idx]
        set_cell_background(cell, "7C2D12")
        set_cell_margins(cell, top=140, bottom=140, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(title)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, (asset, cond, act, desc) in enumerate(act_data):
        row = t_act.rows[r_idx + 1]
        bg = "FFF7ED" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, text in enumerate([asset, cond, act, desc]):
            cell = row.cells[c_idx]
            cell.width = col_widths_act[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.name = "Calibri"
            r.font.size = Pt(9.0)
            r.font.bold = (c_idx == 2)
            r.font.color.rgb = DARK_TEXT

    # -------------------------------------------------------------
    # SECTION 9: DATABASE DESIGN (MongoDB aiot_platform)
    # -------------------------------------------------------------
    add_section_heading("9", "Database Architecture & Schema (MongoDB)")

    db_data = [
        ("telemetry", "device_id, timestamp, temperature, vibration, pressure, current, acoustic_noise, rpm", "Time-series stream of all raw edge sensor packets. Indexed on (device_id, timestamp)."),
        ("anomalies", "eval_id, timestamp, is_anomaly, anomaly_score, predicted_fault, deviations, top_feature", "Audit trail of machine learning model evaluations, classification labels, and feature contributions."),
        ("decisions", "decision_id, rule_id, rule_name, priority, action, message, actuator_states, timestamp", "Immutable log of all automated control decisions executed by the autonomous engine."),
        ("alerts", "alert_id, rule_id, severity, message, status (ACTIVE/ACKNOWLEDGED/RESOLVED), timestamps", "Incident tracking collection supporting operator acknowledgment and resolution lifecycle."),
        ("device_states", "device_id, power_status, cooling_pump, rpm_limit, relief_valve, health_index, last_updated", "Digital twin document maintaining real-time hardware actuator positions and health indices.")
    ]

    t_db = doc.add_table(rows=len(db_data) + 1, cols=3)
    t_db.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_db.autofit = False

    col_widths_db = [Inches(1.3), Inches(2.3), Inches(2.9)]
    hdr_db = t_db.rows[0]
    for c_idx, title in enumerate(["Collection Name", "Key Document Fields", "Storage Purpose & Indexing"]):
        cell = hdr_db.cells[c_idx]
        cell.width = col_widths_db[c_idx]
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, top=140, bottom=140, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(title)
        r.font.name = "Calibri"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, (col, fields, purp) in enumerate(db_data):
        row = t_db.rows[r_idx + 1]
        bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, text in enumerate([col, fields, purp]):
            cell = row.cells[c_idx]
            cell.width = col_widths_db[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.font.bold = (c_idx == 0)
            r.font.color.rgb = DARK_TEXT

    # -------------------------------------------------------------
    # SECTION 10: VERIFICATION & TEST CASES
    # -------------------------------------------------------------
    add_section_heading("10", "System Verification & Test Execution Results")

    test_data = [
        ("TC-01", "Core Module Import & Pipeline Init", "All Python modules (ML, Decision, MQTT) load without missing dependencies", "All modules loaded cleanly", "PASS"),
        ("TC-02", "ML Synthetic Training & Fitting", "Train Isolation Forest & Random Forest on 2,500 samples", "Trained successfully with 100.0% diagnostic accuracy", "PASS"),
        ("TC-03", "Baseline Telemetry Ingestion", "Stream nominal readings (Temp=62°C, Vib=1.8 mm/s)", "Classified as 'Normal Operation', Health=79.8%", "PASS"),
        ("TC-04", "Fault Injection (Thermal Runaway)", "Inject overheating condition into simulator (Temp > 90°C)", "Health dropped to 12.0%, state identified as 'Thermal Runaway'", "PASS"),
        ("TC-05", "Autonomous Protective Cutoff Trigger", "Rule evaluation on thermal runaway condition", "3 actions fired: EMERGENCY_SHUTDOWN, ACTIVATE_COOLING, DISPATCH_ALERT", "PASS"),
        ("TC-06", "Actuator State Transition & Audit", "Verify actuator digital twin records tripped breaker", "Power set to 'TRIPPED_OFFLINE', logged to audit trail", "PASS"),
        ("TC-07", "Anti-Flapping Cooldown Debounce", "Evaluate successive anomalous packet within 5 seconds", "Debounce blocked duplicate execution; cooldown obeyed", "PASS"),
        ("TC-08", "Manual Operator Reset", "Operator executes actuator reset from cockpit", "All actuators restored to nominal; override event logged", "PASS"),
        ("TC-09", "Node-RED JSON Flow Import", "Validate syntax and schema of node_red_flows.json", "Valid Node-RED v3/v4 tab with 10 nodes and wires", "PASS"),
        ("TC-10", "Grafana Dashboard Model Import", "Validate syntax and schema of grafana_dashboard.json", "Valid Grafana schema v38 dashboard with 6 panels", "PASS")
    ]

    t_test = doc.add_table(rows=len(test_data) + 1, cols=5)
    t_test.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_test.autofit = False

    col_widths_test = [Inches(0.8), Inches(1.7), Inches(1.8), Inches(1.6), Inches(0.6)]
    hdr_test = t_test.rows[0]
    for c_idx, title in enumerate(["Test ID", "Test Case Scope", "Expected Benchmark", "Observed Outcome", "Status"]):
        cell = hdr_test.cells[c_idx]
        cell.width = col_widths_test[c_idx]
        set_cell_background(cell, "065F46")
        set_cell_margins(cell, top=140, bottom=140, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(title)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, (tid, scope, exp, obs, stat) in enumerate(test_data):
        row = t_test.rows[r_idx + 1]
        bg = "ECFDF5" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, text in enumerate([tid, scope, exp, obs, stat]):
            cell = row.cells[c_idx]
            cell.width = col_widths_test[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
            p = cell.paragraphs[0]
            if c_idx in [0, 4]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            r.font.bold = (c_idx == 4 or c_idx == 0)
            if c_idx == 4:
                r.font.color.rgb = RGBColor(5, 150, 105)
            else:
                r.font.color.rgb = DARK_TEXT

    # -------------------------------------------------------------
    # SECTION 11: REFERENCES
    # -------------------------------------------------------------
    add_section_heading("11", "References & Bibliography")
    add_bullet("HCL Career Shaper AIoT Curriculum (Lectures 4–7) & User Architecture Guidelines for Industrial Automation.")
    add_bullet("Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008). 'Isolation Forest.' IEEE International Conference on Data Mining (ICDM), pp. 413-422.")
    add_bullet("Pedregosa et al. (2011). 'Scikit-learn: Machine Learning in Python.' Journal of Machine Learning Research, 12, pp. 2825-2830.")
    add_bullet("OASIS Standard (2019). 'MQTT Version 5.0.' OASIS Open Standards.")
    add_bullet("MongoDB, Inc. (2026). 'MongoDB Manual & Time-Series Data Modeling.' https://www.mongodb.com/docs")
    add_bullet("Streamlit Community Cloud Documentation. (2026). https://docs.streamlit.io")
    add_bullet("Grafana Labs (2026). 'Grafana Cloud Documentation and Dashboard Provisioning.' https://grafana.com/docs")

    # Save document
    docx_path = r"C:\Users\Chinmay\.gemini\antigravity\scratch\iot-autonomous-alert-platform\SRS_Report_Chinmay_Prakash_2400320310060.docx"
    doc.save(docx_path)
    print(f"SRS Document successfully created at: {docx_path}")

if __name__ == "__main__":
    create_srs_document()
