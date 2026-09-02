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
        port = np.random.choice([80, 443, 8080, 53, 22]) # Add more ports to overlap
        proto = np.random.choice([0, 1, 2], p=[0.7, 0.2, 0.1])
        # Include some large safe packets (e.g. video streaming, large downloads)
        size = np.random.normal(1500, 3000) if np.random.rand() < 0.1 else np.random.normal(500, 300)
        # Include some very short and very long safe durations
        duration = np.random.exponential(5.0) 
        data.append([port, proto, max(40, size), max(0.01, duration)])
        labels.append(0)
        
    # 2. DDoS (20% of data)
    n_ddos = int(n_samples * 0.2)
    for _ in range(n_ddos):
        port = np.random.choice([80, 443, 53, 123, 445])
        proto = np.random.choice([0, 1, 2], p=[0.4, 0.4, 0.2])
        # Sometimes DDoS packets aren't perfectly small
        size = np.random.normal(100, 200) if np.random.rand() < 0.8 else np.random.normal(1000, 500)
        duration = np.random.uniform(0.001, 0.1) if np.random.rand() < 0.9 else np.random.uniform(0.1, 2.0)
        data.append([port, proto, max(40, size), max(0.001, duration)])
        labels.append(1)
        
    # 3. Data Exfiltration (10% of data)
    n_exfil = int(n_samples * 0.1)
    for _ in range(n_exfil):
        port = np.random.choice([443, 21, 22, 53, 80, 8080]) 
        proto = np.random.choice([0, 1], p=[0.8, 0.2])
        size = np.random.normal(12000, 8000) # Unusually large, but overlaps with safe large packets
        duration = np.random.uniform(2.0, 40.0)
        data.append([port, proto, max(40, size), max(0.1, duration)])
        labels.append(2)
        
    # 4. Unauthorized Tunneling (10% of data)
    n_tunnel = int(n_samples * 0.1)
    for _ in range(n_tunnel):
        port = np.random.choice([53, 22, 443, 3389, 80])
        proto = np.random.choice([0, 1], p=[0.6, 0.4])
        size = np.random.normal(500, 400) # Normal looking size
        duration = np.random.normal(50.0, 30.0) # Very long steady flow
        data.append([port, proto, max(40, size), max(1.0, duration)])
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
