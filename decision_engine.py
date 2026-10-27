"""
Autonomous Decision and Alert Management Engine (AIDAME)
Handles user-configurable rules, autonomous actuator commands, webhook/telegram notifications,
and immutable decision audit trails.
"""

import time
import json
import requests
from datetime import datetime

DEFAULT_RULES = [
    {
        "id": "RULE_01",
        "name": "Thermal Runaway Emergency Cutoff",
        "enabled": True,
        "priority": "CRITICAL",
        "conditions": {
            "temperature_gt": 90.0,
            "require_ml_anomaly": True
        },
        "action": "EMERGENCY_SHUTDOWN",
        "action_param": "asset/motor_01/control/power",
        "message": "Thermal runaway detected (>90°C with ML anomaly). Initiated emergency motor trip.",
        "cooldown_seconds": 30
    },
    {
        "id": "RULE_02",
        "name": "Bearing Failure - Speed Throttling",
        "enabled": True,
        "priority": "HIGH",
        "conditions": {
            "vibration_gt": 4.5,
            "acoustic_noise_gt": 80.0
        },
        "action": "THROTTLE_MOTOR",
        "action_param": "asset/motor_01/control/rpm_limit",
        "message": "High vibration and acoustic noise. Throttling motor speed to 50% to prevent seizure.",
        "cooldown_seconds": 45
    },
    {
        "id": "RULE_03",
        "name": "Auxiliary Cooling Activation",
        "enabled": True,
        "priority": "MEDIUM",
        "conditions": {
            "temperature_gt": 78.0
        },
        "action": "ACTIVATE_COOLING",
        "action_param": "asset/motor_01/control/cooling_pump",
        "message": "Temperature elevated above 78°C. Auxiliary liquid cooling valve opened 100%.",
        "cooldown_seconds": 20
    },
    {
        "id": "RULE_04",
        "name": "Cavitation Pressure Relief",
        "enabled": True,
        "priority": "HIGH",
        "conditions": {
            "pressure_gt": 6.0
        },
        "action": "PRESSURE_RELIEF",
        "action_param": "asset/motor_01/control/relief_valve",
        "message": "Hydraulic pressure exceeded 6.0 bar. Pressure relief bypass solenoid opened.",
        "cooldown_seconds": 30
    },
    {
        "id": "RULE_05",
        "name": "Predictive Health Degradation Alert",
        "enabled": True,
        "priority": "WARNING",
        "conditions": {
            "health_index_lt": 45.0
        },
        "action": "DISPATCH_ALERT",
        "action_param": "webhook_or_mqtt",
        "message": "Machine Health Index dropped below 45%. Maintenance ticket auto-generated.",
        "cooldown_seconds": 60
    }
]

class AutonomousDecisionEngine:
    def __init__(self, rules=None):
        self.rules = rules if rules is not None else [r.copy() for r in DEFAULT_RULES]
        self.audit_log = []
        self.last_triggered = {}  # rule_id -> timestamp
        self.actuator_states = {
            "power": "ONLINE",
            "cooling_pump": "STANDBY",
            "rpm_limit": 100,
            "relief_valve": "CLOSED",
            "last_autonomous_action": "None"
        }

    def evaluate(self, telemetry, ml_result, mqtt_client=None, webhook_url=None, telegram_config=None):
        """
        Evaluate current sensor telemetry + ML prediction against all active rules.
        Returns list of executed actions during this tick.
        """
        now = time.time()
        executed_actions = []

        for rule in self.rules:
            if not rule.get("enabled", True):
                continue

            rule_id = rule["id"]
            cooldown = rule.get("cooldown_seconds", 30)

            # Check cooldown debounce
            if rule_id in self.last_triggered:
                if now - self.last_triggered[rule_id] < cooldown:
                    continue

            # Evaluate conditions
            conds = rule.get("conditions", {})
            matched = True

            # Temperature checks
            if "temperature_gt" in conds and telemetry.get("temperature", 0) <= conds["temperature_gt"]:
                matched = False
            if "temperature_lt" in conds and telemetry.get("temperature", 0) >= conds["temperature_lt"]:
                matched = False

            # Vibration checks
            if "vibration_gt" in conds and telemetry.get("vibration", 0) <= conds["vibration_gt"]:
                matched = False

            # Pressure checks
            if "pressure_gt" in conds and telemetry.get("pressure", 0) <= conds["pressure_gt"]:
                matched = False
            if "pressure_lt" in conds and telemetry.get("pressure", 0) >= conds["pressure_lt"]:
                matched = False

            # Current checks
            if "current_gt" in conds and telemetry.get("current", 0) <= conds["current_gt"]:
                matched = False

            # Acoustic noise checks
            if "acoustic_noise_gt" in conds and telemetry.get("acoustic_noise", 0) <= conds["acoustic_noise_gt"]:
                matched = False

            # ML Anomaly check
            if conds.get("require_ml_anomaly", False) and not ml_result.get("is_anomaly", False):
                matched = False

            # Health index check
            if "health_index_lt" in conds and ml_result.get("health_index", 100) >= conds["health_index_lt"]:
                matched = False

            if matched:
                # Trigger action!
                self.last_triggered[rule_id] = now
                action_type = rule.get("action", "DISPATCH_ALERT")
                action_result = self._execute_action(
                    rule, telemetry, ml_result, mqtt_client, webhook_url, telegram_config
                )
                executed_actions.append(action_result)

        return executed_actions

    def _execute_action(self, rule, telemetry, ml_result, mqtt_client, webhook_url, telegram_config):
        action_type = rule.get("action")
        target_param = rule.get("action_param", "")
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update simulated hardware actuator states
        if action_type == "EMERGENCY_SHUTDOWN":
            self.actuator_states["power"] = "TRIPPED_OFFLINE"
            self.actuator_states["last_autonomous_action"] = f"Trip Motor Breaker ({rule['id']})"
        elif action_type == "ACTIVATE_COOLING":
            self.actuator_states["cooling_pump"] = "RUNNING_100%"
            self.actuator_states["last_autonomous_action"] = f"Cooling Boost ({rule['id']})"
        elif action_type == "THROTTLE_MOTOR":
            self.actuator_states["rpm_limit"] = 50
            self.actuator_states["last_autonomous_action"] = f"RPM Throttled to 50% ({rule['id']})"
        elif action_type == "PRESSURE_RELIEF":
            self.actuator_states["relief_valve"] = "OPEN_BYPASS"
            self.actuator_states["last_autonomous_action"] = f"Relief Valve Dump ({rule['id']})"

        # Dispatch via MQTT if connected
        mqtt_dispatched = False
        if mqtt_client and mqtt_client.is_connected:
            try:
                cmd_topic = f"iot/actuator/{target_param}"
                cmd_payload = json.dumps({
                    "action": action_type,
                    "rule_id": rule["id"],
                    "timestamp": timestamp_str,
                    "target_state": self.actuator_states
                })
                mqtt_client.publish(cmd_topic, cmd_payload)
                mqtt_dispatched = True
            except Exception as e:
                pass

        # Dispatch Webhook if provided
        webhook_status = "Skipped"
        if webhook_url and webhook_url.strip():
            try:
                payload = {
                    "event": "AUTONOMOUS_IOT_ALERT",
                    "rule": rule["name"],
                    "priority": rule["priority"],
                    "message": rule["message"],
                    "telemetry": telemetry,
                    "ml_diagnosis": ml_result["predicted_fault"],
                    "health_index": ml_result["health_index"],
                    "timestamp": timestamp_str
                }
                res = requests.post(webhook_url, json=payload, timeout=2.5)
                webhook_status = f"Dispatched (HTTP {res.status_code})"
            except Exception as e:
                webhook_status = f"Failed ({str(e)[:30]})"

        # Record in audit log
        log_entry = {
            "timestamp": timestamp_str,
            "rule_id": rule["id"],
            "rule_name": rule["name"],
            "priority": rule["priority"],
            "action": action_type,
            "message": rule["message"],
            "machine_health": f"{ml_result.get('health_index', 0)}%",
            "fault_diagnosis": ml_result.get("predicted_fault", "Unknown"),
            "mqtt_dispatched": mqtt_dispatched,
            "webhook_status": webhook_status
        }
        self.audit_log.insert(0, log_entry)  # newest first
        if len(self.audit_log) > 200:
            self.audit_log.pop()

        return log_entry

    def reset_actuators(self):
        """User manual override to reset tripped actuators back to safe normal."""
        self.actuator_states = {
            "power": "ONLINE",
            "cooling_pump": "STANDBY",
            "rpm_limit": 100,
            "relief_valve": "CLOSED",
            "last_autonomous_action": "Manual Override / Reset"
        }
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rule_id": "MANUAL_OVERRIDE",
            "rule_name": "Operator System Reset",
            "priority": "INFO",
            "action": "RESET_ACTUATORS",
            "message": "Operator acknowledged alerts and restored actuators to normal baseline.",
            "machine_health": "N/A",
            "fault_diagnosis": "Operator Action",
            "mqtt_dispatched": True,
            "webhook_status": "Logged"
        }
        self.audit_log.insert(0, entry)

    def add_rule(self, rule_dict):
        self.rules.append(rule_dict)

    def delete_rule(self, rule_id):
        self.rules = [r for r in self.rules if r["id"] != rule_id]

    def update_rule(self, updated_rule):
        for idx, r in enumerate(self.rules):
            if r["id"] == updated_rule["id"]:
                self.rules[idx] = updated_rule
                break
