import os
import time
import joblib
import numpy as np
from typing import Dict, Tuple

class MLEngine:
    def __init__(self):
        # Load trained models
        models_dir = os.path.join(os.path.dirname(__file__), '../models/trained')
        rf_path = os.path.join(models_dir, 'rf_classifier.pkl')
        iso_path = os.path.join(models_dir, 'isolation_forest.pkl')
        
        try:
            self.rf_clf = joblib.load(rf_path)
            self.iso_forest = joblib.load(iso_path)
            print("Successfully loaded ML models.")
        except FileNotFoundError:
            print("WARNING: Models not found. Run train_model.py first.")
            self.rf_clf = None
            self.iso_forest = None
            
        # Label mapping matching train_model.py
        self.label_map = {
            0: "Safe",
            1: "DDoS",
            2: "Data Exfiltration",
            3: "Unauthorized Tunneling"
        }

        # Confidence-Decay Mechanism State
        self.anomaly_history: Dict[str, list] = {}
        self.decay_factor = 0.85 

    def _update_anomaly_history(self, source_ip: str, timestamp: float, is_malicious: bool):
        if source_ip not in self.anomaly_history:
            self.anomaly_history[source_ip] = []
        
        current_time = time.time()
        self.anomaly_history[source_ip] = [
            record for record in self.anomaly_history[source_ip] 
            if current_time - record['time'] < 600
        ]
        
        self.anomaly_history[source_ip].append({
            'time': timestamp,
            'is_malicious': is_malicious
        })

    def _calculate_confidence_decay(self, source_ip: str, base_confidence: float) -> float:
        history = self.anomaly_history.get(source_ip, [])
        if not history:
            return base_confidence
            
        recent_anomalies = len(history)
        if recent_anomalies > 5:
            decay_multiplier = max(0.3, self.decay_factor ** (recent_anomalies - 5))
            return base_confidence * decay_multiplier
            
        return base_confidence

    def _generate_explanation(self, category: str, threat_type: str, packet: dict) -> str:
        if category == "Safe":
            return "Traffic aligns with historical baseline. Model confirms normal behavior."
            
        explanations = []
        if threat_type == "DDoS":
            if packet['packet_size'] < 100:
                explanations.append(f"Model detected high volume of small packets ({packet['packet_size']} bytes).")
            if packet['flow_duration'] < 0.1:
                explanations.append(f"Abnormally short flow duration ({packet['flow_duration']:.3f}s) indicates flood attack pattern.")
            
        elif threat_type == "Data Exfiltration":
            if packet['packet_size'] > 5000:
                explanations.append(f"Model identified unusually large payload ({packet['packet_size']} bytes) for this protocol.")
            explanations.append("Prolonged outbound flow strongly deviates from standard user behavior.")
            
        elif threat_type == "Unauthorized Tunneling":
            explanations.append(f"Encrypted traffic characteristics found on unexpected port ({packet['dest_port']}).")
            explanations.append("Model matched flow timing signatures to known tunneling protocols.")
            
        else:
            explanations.append(f"Random Forest and Isolation Forest detected a severe statistical deviation.")

        return " ".join(explanations)

    def analyze_packet(self, packet_dict: dict) -> Tuple[float, str, str, str, float]:
        """
        Runs ML Inference using the real trained RandomForest and IsolationForest.
        Returns: (threat_score, category, threat_type, explanation, final_confidence)
        """
        # Feature extraction
        port = packet_dict.get('dest_port', 80)
        protocol_str = packet_dict.get('protocol', 'TCP')
        # Encode protocol
        proto_map = {"TCP": 0, "UDP": 1, "ICMP": 2}
        proto_encoded = proto_map.get(protocol_str, 0)
        
        size = packet_dict.get('packet_size', 500)
        duration = packet_dict.get('flow_duration', 1.0)
        
        # Prepare feature vector [dest_port, protocol_encoded, packet_size, flow_duration]
        X = np.array([[port, proto_encoded, size, duration]])
        
        # Base safe defaults in case models aren't loaded
        if self.rf_clf is None:
            return 0.1, "Safe", None, "Model not loaded.", 0.99
            
        # Predict Probabilities
        probas = self.rf_clf.predict_proba(X)[0] # e.g. [0.1, 0.8, 0.05, 0.05]
        predicted_class_idx = np.argmax(probas)
        base_confidence = float(probas[predicted_class_idx])
        
        # Unsupervised Anomaly Score (-1 for anomaly, 1 for normal)
        iso_pred = self.iso_forest.predict(X)[0]
        iso_score = self.iso_forest.score_samples(X)[0] # lower score means more anomalous
        
        threat_type_str = self.label_map[predicted_class_idx]
        
        if threat_type_str == "Safe":
            # If Random Forest says safe, but Isolation Forest strongly disagrees
            if iso_pred == -1:
                category = "Suspicious"
                threat_score = 0.4
                threat_type_str = "Unknown Anomaly"
            else:
                category = "Safe"
                threat_score = 1.0 - base_confidence
                threat_type_str = None
        else:
            threat_score = base_confidence # Threat score is how confident it is about the attack
            if threat_score > 0.7:
                category = "Malicious"
            else:
                category = "Suspicious"
        
        # Apply Confidence-Decay
        final_confidence = self._calculate_confidence_decay(packet_dict.get('source_ip', ''), base_confidence)
        
        # Downgrade a Suspicious/Malicious event due to low confidence
        if final_confidence < 0.4 and category != "Safe":
            if category == "Malicious":
                category = "Suspicious"
            else:
                category = "Safe"
                threat_type_str = None
            threat_score *= 0.5 
            
        # Update history
        self._update_anomaly_history(packet_dict.get('source_ip', ''), time.time(), category == "Malicious")
        
        # Generate Explanation
        explanation = self._generate_explanation(category, threat_type_str, packet_dict)
        
        return threat_score, category, threat_type_str, explanation, final_confidence

ml_engine = MLEngine()
