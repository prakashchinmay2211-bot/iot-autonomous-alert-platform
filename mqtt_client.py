"""
MQTT Client and Telemetry Engine for IoT Autonomous Decision Platform
Supports:
- HiveMQ Cloud (TLS 8883)
- EMQX / Eclipse Mosquitto
- Local / Enterprise Brokers
- Built-in High-Fidelity Physics Simulator with Fault Injection
"""

import time
import json
import random
import threading
from collections import deque

try:
    import paho.mqtt.client as mqtt
    from paho.mqtt.enums import CallbackAPIVersion
    PAHO_V2 = True
except Exception:
    import paho.mqtt.client as mqtt
    PAHO_V2 = False

class IoTTelemetrySimulator:
    """Simulates realistic industrial physical system with optional fault injection."""
    def __init__(self):
        self.mode = "Normal"
        self.step_count = 0
        # Baselines
        self.temp = 62.0
        self.vib = 1.8
        self.press = 4.2
        self.curr = 12.5
        self.acoust = 68.0
        self.rpm = 1750.0

    def set_fault_mode(self, mode):
        """Set simulation mode: 'Normal', 'Bearing Wear', 'Overheating', 'Cavitation', 'Overload', 'Random Noise'"""
        self.mode = mode

    def next_sample(self):
        self.step_count += 1
        t = self.step_count * 0.1

        # Base sinusoidal physical variations
        base_t = 62.0 + 1.5 * random.gauss(0, 0.4)
        base_v = 1.8 + 0.15 * random.gauss(0, 0.2)
        base_p = 4.2 + 0.1 * random.gauss(0, 0.1)
        base_c = 12.5 + 0.3 * random.gauss(0, 0.3)
        base_a = 68.0 + 1.2 * random.gauss(0, 0.5)
        base_r = 1750.0 + 5.0 * random.gauss(0, 2.0)

        if self.mode == "Bearing Wear":
            # High vibration, high acoustic noise, slight heat rise
            base_v += 4.2 + random.uniform(-0.5, 0.8)
            base_a += 20.0 + random.uniform(-2, 4)
            base_t += 12.0
            base_r -= 35.0
        elif self.mode == "Overheating":
            # Extreme temp, high current
            base_t += 36.0 + random.uniform(-2, 5)
            base_c += 7.0 + random.uniform(-0.5, 1.2)
            base_p += 1.3
        elif self.mode == "Cavitation":
            # Pressure spikes, erratic vibration
            base_p += 2.8 + random.uniform(-1.5, 2.0)
            base_v += 3.2 + random.uniform(-0.8, 1.5)
            base_a += 14.0
        elif self.mode == "Overload":
            # High current, RPM drop, severe heat
            base_c += 13.5 + random.uniform(-1, 2)
            base_r -= 200.0 + random.uniform(-30, 20)
            base_t += 24.0
            base_v += 2.6
        elif self.mode == "Random Noise":
            base_t += random.uniform(-8, 15)
            base_v += random.uniform(-0.5, 3.0)
            base_p += random.uniform(-1.0, 2.0)
            base_c += random.uniform(-3.0, 8.0)

        return {
            "device_id": "PUMP_TURBINE_01",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "temperature": round(max(20.0, base_t), 2),
            "vibration": round(max(0.1, base_v), 2),
            "pressure": round(max(0.5, base_p), 2),
            "current": round(max(1.0, base_c), 2),
            "acoustic_noise": round(max(30.0, base_a), 2),
            "rpm": round(max(0.0, base_r), 1),
            "simulation_mode": self.mode
        }


class MQTTHandler:
    def __init__(self, broker="broker.hivemq.com", port=1883, username=None, password=None, use_tls=False):
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.is_connected = False
        self.incoming_queue = deque(maxlen=200)
        self.client = None
        self.simulator = IoTTelemetrySimulator()

    def connect(self):
        try:
            client_id = f"aidams_client_{random.randint(1000, 9999)}"
            if PAHO_V2:
                self.client = mqtt.Client(CallbackAPIVersion.VERSION2, client_id=client_id)
            else:
                self.client = mqtt.Client(client_id=client_id)

            if self.username and self.password:
                self.client.username_pw_set(self.username, self.password)

            if self.use_tls:
                self.client.tls_set()

            self.client.on_connect = self._on_connect
            self.client.on_disconnect = self._on_disconnect
            self.client.on_message = self._on_message

            self.client.connect_async(self.broker, self.port, keepalive=60)
            self.client.loop_start()
            return True, "MQTT Loop started successfully"
        except Exception as e:
            self.is_connected = False
            return False, f"MQTT connection failed: {str(e)}"

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            self.is_connected = True
            client.subscribe("iot/telemetry/#")
            client.subscribe("iot/actuator/#")
        else:
            self.is_connected = False

    def _on_disconnect(self, client, userdata, rc, properties=None):
        self.is_connected = False

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            self.incoming_queue.append({
                "topic": msg.topic,
                "payload": payload,
                "received_at": time.time()
            })
        except Exception:
            pass

    def publish(self, topic, payload_dict_or_str):
        if not self.is_connected or not self.client:
            return False
        try:
            if isinstance(payload_dict_or_str, dict):
                body = json.dumps(payload_dict_or_str)
            else:
                body = str(payload_dict_or_str)
            self.client.publish(topic, body, qos=1)
            return True
        except Exception:
            return False

    def disconnect(self):
        if self.client:
            try:
                self.client.loop_stop()
                self.client.disconnect()
            except Exception:
                pass
        self.is_connected = False
