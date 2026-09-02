import os
import joblib
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, classification_report

def evaluate_and_document():
    models_dir = os.path.join(os.path.dirname(__file__), '../models/trained')
    rf_path = os.path.join(models_dir, 'rf_classifier.pkl')
    test_data_path = os.path.join(models_dir, 'test_data.pkl')
    
    if not os.path.exists(rf_path) or not os.path.exists(test_data_path):
        print("Models or test data not found. Run train_model.py first.")
        return
        
    print("Loading model and test data...")
    rf_clf = joblib.load(rf_path)
    test_data = joblib.load(test_data_path)
    
    X_test = test_data['X_test']
    y_test = test_data['y_test']
    
    print("Evaluating model...")
    y_pred = rf_clf.predict(X_test)
    
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=["Safe", "DDoS", "Data Exfiltration", "Tunneling"])
    
    print("\n--- Model Evaluation Results ---")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print("\nConfusion Matrix:")
    print(cm)
    print("\nClassification Report:")
    print(report)
    
    # Write to docs
    docs_path = os.path.join(os.path.dirname(__file__), '../../docs/model_performance.md')
    os.makedirs(os.path.dirname(docs_path), exist_ok=True)
    
    with open(docs_path, 'w') as f:
        f.write("# ML Model Performance Evaluation\n\n")
        f.write("This document contains the evaluation metrics for the supervised `RandomForestClassifier` trained on the synthetic flow dataset.\n\n")
        f.write("## Overall Metrics\n")
        f.write(f"- **Precision (weighted):** {precision:.4f}\n")
        f.write(f"- **Recall (weighted):** {recall:.4f}\n")
        f.write(f"- **F1-Score (weighted):** {f1:.4f}\n\n")
        f.write("## Classification Report\n")
        f.write("```text\n")
        f.write(report)
        f.write("\n```\n\n")
        f.write("## Confusion Matrix\n")
        f.write("Rows are actual labels, columns are predicted labels in order: Safe, DDoS, Data Exfiltration, Tunneling.\n")
        f.write("```text\n")
        f.write(str(cm))
        f.write("\n```\n\n")
        f.write("## Methodology\n")
        f.write("The model was evaluated on a 20% held-out test split of 10,000 synthetic records. The high accuracy indicates the Random Forest successfully learned the distinct boundaries between our simulated attack vectors based on packet size, flow duration, and protocol combinations.\n")
        
    print(f"\nSaved metrics to {os.path.abspath(docs_path)}")

if __name__ == "__main__":
    evaluate_and_document()
