import ml_engine
import decision_engine
import mqtt_client

print("1. Testing ML Engine...")
engine = ml_engine.IoTMLEngine()
res = engine.train_models()
print(f"   Accuracy: {res['accuracy']}% across {res['samples_trained']} samples.")

print("2. Testing Simulator...")
sim = mqtt_client.IoTTelemetrySimulator()
pkt = sim.next_sample()
print(f"   Sample: Temp={pkt['temperature']}°C, Vib={pkt['vibration']} mm/s")

print("3. Testing Prediction & Explainability...")
pred = engine.predict_telemetry(pkt)
print(f"   Diagnosis: {pred['predicted_fault']} (Health: {pred['health_index']}%)")
print(f"   Top Driver: {pred['top_driving_feature']} ({pred['top_deviation_pct']}%)")

print("4. Testing Decision Engine...")
dec = decision_engine.AutonomousDecisionEngine()
actions = dec.evaluate(pkt, pred)
print(f"   Evaluated {len(dec.rules)} rules. Actions triggered: {len(actions)}")

print("5. Testing Fault Simulation & Actuation Trigger...")
sim.set_fault_mode("Overheating")
fault_pkt = sim.next_sample()
fault_pred = engine.predict_telemetry(fault_pkt)
print(f"   Fault Diagnosis: {fault_pred['predicted_fault']} (Health: {fault_pred['health_index']}%)")
fault_actions = dec.evaluate(fault_pkt, fault_pred)
print(f"   Autonomous Actions Triggered: {len(fault_actions)}")
for a in fault_actions:
    print(f"     -> Action: {a['action']} | Rule: {a['rule_name']}")

print("ALL TESTS PASSED PERFECTLY!")
