"""
Machine Learning Engine for Autonomous IoT Decision and Alert Management
Includes:
- Synthetic IoT Telemetry Generator with realistic physics & fault injection
- Isolation Forest for Unsupervised Anomaly Detection
- Random Forest Classifier for Multi-Class Failure Diagnosis & Predictive Maintenance
- Health Index & Failure Risk Probability Scoring
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

FAULT_CLASSES = {
    0: "Normal Operation",
    1: "Bearing Degradation",
    2: "Thermal Runaway / Cooling Failure",
    3: "Cavitation / Pressure Surge",
    4: "Motor Overload / Electrical Fault"
}

FEATURE_COLS = ["temperature", "vibration", "pressure", "current", "acoustic_noise", "rpm"]

class IoTMLEngine:
    def __init__(self, model_dir=None):
        self.model_dir = model_dir or os.path.dirname(__file__)
        self.scaler = StandardScaler()
        self.anomaly_model = None
        self.classifier_model = None
        self.is_trained = False
        self.metrics = {}

    def generate_synthetic_data(self, n_samples=2500, random_state=42):
        """Generate realistic industrial telemetry dataset with 5 operational states."""
        np.random.seed(random_state)
        samples_per_class = n_samples // 5

        data = []
        labels = []

        # 0: Normal
        t0 = np.random.normal(62.0, 3.5, samples_per_class)
        v0 = np.random.normal(1.8, 0.4, samples_per_class)
        p0 = np.random.normal(4.2, 0.25, samples_per_class)
        c0 = np.random.normal(12.5, 1.0, samples_per_class)
        a0 = np.random.normal(68.0, 3.0, samples_per_class)
        r0 = np.random.normal(1750, 15, samples_per_class)
        for i in range(samples_per_class):
            data.append([t0[i], v0[i], p0[i], c0[i], a0[i], r0[i]])
            labels.append(0)

        # 1: Bearing Degradation (High vibration, high acoustic noise, mild temp rise)
        t1 = np.random.normal(74.0, 4.0, samples_per_class)
        v1 = np.random.normal(5.8, 1.2, samples_per_class)
        p1 = np.random.normal(4.1, 0.3, samples_per_class)
        c1 = np.random.normal(14.0, 1.2, samples_per_class)
        a1 = np.random.normal(86.0, 4.5, samples_per_class)
        r1 = np.random.normal(1720, 25, samples_per_class)
        for i in range(samples_per_class):
            data.append([t1[i], v1[i], p1[i], c1[i], a1[i], r1[i]])
            labels.append(1)

        # 2: Thermal Runaway / Cooling Failure (Very high temp, high current)
        t2 = np.random.normal(96.0, 6.0, samples_per_class)
        v2 = np.random.normal(2.6, 0.6, samples_per_class)
        p2 = np.random.normal(5.4, 0.5, samples_per_class)
        c2 = np.random.normal(19.5, 2.0, samples_per_class)
        a2 = np.random.normal(74.0, 3.5, samples_per_class)
        r2 = np.random.normal(1680, 40, samples_per_class)
        for i in range(samples_per_class):
            data.append([t2[i], v2[i], p2[i], c2[i], a2[i], r2[i]])
            labels.append(2)

        # 3: Cavitation / Pressure Surge (High pressure fluctuations, sharp vibration spikes)
        t3 = np.random.normal(68.0, 4.0, samples_per_class)
        v3 = np.random.normal(4.8, 1.0, samples_per_class)
        p3 = np.random.normal(6.8, 0.9, samples_per_class)
        c3 = np.random.normal(13.8, 1.5, samples_per_class)
        a3 = np.random.normal(80.0, 5.0, samples_per_class)
        r3 = np.random.normal(1740, 30, samples_per_class)
        for i in range(samples_per_class):
            data.append([t3[i], v3[i], p3[i], c3[i], a3[i], r3[i]])
            labels.append(3)

        # 4: Motor Overload / Electrical Fault (Very high current, RPM drop, high vibration)
        t4 = np.random.normal(85.0, 5.0, samples_per_class)
        v4 = np.random.normal(4.2, 0.8, samples_per_class)
        p4 = np.random.normal(4.6, 0.4, samples_per_class)
        c4 = np.random.normal(25.5, 2.5, samples_per_class)
        a4 = np.random.normal(83.0, 4.0, samples_per_class)
        r4 = np.random.normal(1560, 50, samples_per_class)
        for i in range(samples_per_class):
            data.append([t4[i], v4[i], p4[i], c4[i], a4[i], r4[i]])
            labels.append(4)

        df = pd.DataFrame(data, columns=FEATURE_COLS)
        df["fault_code"] = labels
        df["fault_name"] = [FAULT_CLASSES[c] for c in labels]
        return df

    def train_models(self, contamination=0.15, n_estimators=100):
        """Train Isolation Forest and Random Forest Classifier."""
        df = self.generate_synthetic_data()
        X = df[FEATURE_COLS]
        y = df["fault_code"]

        # Scale features
        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)

        # 1. Isolation Forest for unsupervised anomaly detection
        self.anomaly_model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=n_estimators
        )
        self.anomaly_model.fit(X_scaled)

        # 2. Random Forest for supervised failure classification
        self.classifier_model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=10,
            random_state=42
        )
        self.classifier_model.fit(X_scaled, y)

        # Evaluation
        y_pred = self.classifier_model.predict(X_scaled)
        acc = accuracy_score(y, y_pred)
        self.metrics = {
            "accuracy": round(float(acc) * 100, 2),
            "samples_trained": len(df),
            "contamination": contamination,
            "n_estimators": n_estimators,
            "feature_importances": dict(zip(FEATURE_COLS, [round(float(v), 3) for v in self.classifier_model.feature_importances_]))
        }
        self.is_trained = True
        return self.metrics

    def predict_telemetry(self, sensor_dict):
        """
        Evaluate a single telemetry packet or batch.
        Returns anomaly status, failure classification, probabilities, and health score.
        """
        if not self.is_trained:
            self.train_models()

        row = pd.DataFrame([[
            float(sensor_dict.get("temperature", 65.0)),
            float(sensor_dict.get("vibration", 1.8)),
            float(sensor_dict.get("pressure", 4.2)),
            float(sensor_dict.get("current", 12.5)),
            float(sensor_dict.get("acoustic_noise", 68.0)),
            float(sensor_dict.get("rpm", 1750.0))
        ]], columns=FEATURE_COLS)

        row_scaled = self.scaler.transform(row)

        # Anomaly Detection: 1 = Normal, -1 = Anomaly
        raw_anomaly = self.anomaly_model.predict(row_scaled)[0]
        anomaly_score = self.anomaly_model.score_samples(row_scaled)[0]  # lower means more abnormal
        is_anomaly = bool(raw_anomaly == -1)

        # Multi-class diagnosis
        class_pred = self.classifier_model.predict(row_scaled)[0]
        probs = self.classifier_model.predict_proba(row_scaled)[0]
        prob_dict = {FAULT_CLASSES[i]: round(float(probs[i]) * 100, 1) for i in range(len(probs))}

        # Calculate Health Score (100 = flawless, 0 = critical collapse)
        # Normal class probability is high -> Health is high
        normal_prob = probs[0]
        # Anomaly score typically ranges from -0.8 to 0.0
        normalized_score = np.clip((anomaly_score + 0.65) / 0.5, 0.0, 1.0)
        health_index = round(float((0.6 * normal_prob + 0.4 * normalized_score) * 100), 1)
        health_index = max(1.0, min(100.0, health_index))

        # Failure Risk is inverse of health
        failure_risk = round(100.0 - health_index, 1)

        # Feature deviations to explain anomaly
        baselines = {"temperature": 62.0, "vibration": 1.8, "pressure": 4.2, "current": 12.5, "acoustic_noise": 68.0, "rpm": 1750.0}
        deviations = {}
        for col in FEATURE_COLS:
            val = float(sensor_dict.get(col, baselines[col]))
            diff_pct = ((val - baselines[col]) / baselines[col]) * 100
            deviations[col] = round(diff_pct, 1)

        # Top driving feature
        top_driver = max(deviations.items(), key=lambda x: abs(x[1]))

        return {
            "is_anomaly": is_anomaly,
            "anomaly_score": round(float(anomaly_score), 4),
            "predicted_fault_code": int(class_pred),
            "predicted_fault": FAULT_CLASSES[class_pred],
            "confidence": round(float(probs[class_pred]) * 100, 1),
            "health_index": health_index,
            "failure_risk": failure_risk,
            "class_probabilities": prob_dict,
            "deviations": deviations,
            "top_driving_feature": top_driver[0],
            "top_deviation_pct": top_driver[1]
        }
