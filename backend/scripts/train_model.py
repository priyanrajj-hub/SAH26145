import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split

def generate_synthetic_data(n_samples=5000):
    """
    Generates realistic synthetic flow data.
    Features: dest_port, protocol_encoded, packet_size, flow_duration
    Labels: 0 (Safe), 1 (DDoS), 2 (Data Exfiltration), 3 (Unauthorized Tunneling)
    """
    np.random.seed(42)
    data = []
    labels = []
    
    # Protocols: 0: TCP, 1: UDP, 2: ICMP
    
    # 1. Safe Traffic (60% of data)
    n_safe = int(n_samples * 0.6)
    for _ in range(n_safe):
        port = np.random.choice([80, 443, 8080, 53, 22, 123, 21, 3389]) 
        proto = np.random.choice([0, 1, 2], p=[0.6, 0.3, 0.1])
        # Significant overlap with attacks: some very small, some very large
        size = np.random.normal(1500, 8000) if np.random.rand() < 0.15 else np.random.normal(500, 400)
        duration = np.random.exponential(10.0) if np.random.rand() < 0.2 else np.random.exponential(0.5)
        data.append([port, proto, max(40, size), max(0.001, duration)])
        labels.append(0)
        
    # 2. DDoS (20% of data)
    n_ddos = int(n_samples * 0.2)
    for _ in range(n_ddos):
        port = np.random.choice([80, 443, 53, 123, 445])
        proto = np.random.choice([0, 1, 2], p=[0.4, 0.4, 0.2])
        # Add overlaps: sometimes DDoS packets behave like safe traffic
        size = np.random.normal(500, 300) if np.random.rand() < 0.2 else np.random.normal(100, 50)
        duration = np.random.exponential(5.0) if np.random.rand() < 0.2 else np.random.uniform(0.001, 0.05)
        data.append([port, proto, max(40, size), max(0.001, duration)])
        labels.append(1)
        
    # 3. Data Exfiltration (10% of data)
    n_exfil = int(n_samples * 0.1)
    for _ in range(n_exfil):
        port = np.random.choice([443, 21, 22, 53, 80, 8080]) 
        proto = np.random.choice([0, 1], p=[0.8, 0.2])
        # Overlap with large safe packets, sometimes smaller chunks
        size = np.random.normal(1500, 1000) if np.random.rand() < 0.3 else np.random.normal(12000, 5000)
        duration = np.random.normal(10.0, 5.0) if np.random.rand() < 0.3 else np.random.uniform(20.0, 60.0)
        data.append([port, proto, max(40, size), max(0.1, duration)])
        labels.append(2)
        
    # 4. Unauthorized Tunneling (10% of data)
    n_tunnel = int(n_samples * 0.1)
    for _ in range(n_tunnel):
        port = np.random.choice([53, 22, 443, 3389, 80, 8080])
        proto = np.random.choice([0, 1], p=[0.6, 0.4])
        # Blend in with Safe traffic
        size = np.random.normal(500, 500) 
        duration = np.random.exponential(2.0) if np.random.rand() < 0.2 else np.random.normal(40.0, 20.0)
        data.append([port, proto, max(40, size), max(0.1, duration)])
        labels.append(3)
        
    df = pd.DataFrame(data, columns=['dest_port', 'protocol_encoded', 'packet_size', 'flow_duration'])
    y = np.array(labels)
    
    return df, y

def train_and_save():
    print("Generating synthetic dataset...")
    X, y = generate_synthetic_data(10000)
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training RandomForestClassifier...")
    rf_clf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    rf_clf.fit(X_train, y_train)
    
    print("Training IsolationForest (Unsupervised)...")
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    # Fit only on safe data for better anomaly detection baseline
    X_safe = X_train[y_train == 0]
    iso_forest.fit(X_safe)
    
    # Save models
    models_dir = os.path.join(os.path.dirname(__file__), '../models/trained')
    os.makedirs(models_dir, exist_ok=True)
    
    rf_path = os.path.join(models_dir, 'rf_classifier.pkl')
    iso_path = os.path.join(models_dir, 'isolation_forest.pkl')
    
    joblib.dump(rf_clf, rf_path)
    joblib.dump(iso_forest, iso_path)
    print(f"Models saved to {models_dir}")
    
    # Save test set for evaluate_model.py
    test_data_path = os.path.join(models_dir, 'test_data.pkl')
    joblib.dump({'X_test': X_test, 'y_test': y_test}, test_data_path)
    print("Test split saved for evaluation.")

if __name__ == "__main__":
    train_and_save()
