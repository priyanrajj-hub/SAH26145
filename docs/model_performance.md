# ML Model Performance Evaluation

This document contains the evaluation metrics for the supervised `RandomForestClassifier` trained on the synthetic flow dataset.

## Overall Metrics
- **Precision (weighted):** 0.9410
- **Recall (weighted):** 0.9405
- **F1-Score (weighted):** 0.9395

## Classification Report
```text
                   precision    recall  f1-score   support

             Safe       0.93      0.98      0.95      1198
             DDoS       0.96      0.94      0.95       415
Data Exfiltration       0.96      0.82      0.88       212
        Tunneling       0.94      0.82      0.88       175

         accuracy                           0.94      2000
        macro avg       0.95      0.89      0.92      2000
     weighted avg       0.94      0.94      0.94      2000

```

## Confusion Matrix
Rows are actual labels, columns are predicted labels in order: Safe, DDoS, Data Exfiltration, Tunneling.
```text
[[1172   15    7    4]
 [  24  391    0    0]
 [  32    0  174    6]
 [  30    0    1  144]]
```

## Methodology
The model was evaluated on a 20% held-out test split of 10,000 synthetic records. The high accuracy indicates the Random Forest successfully learned the distinct boundaries between our simulated attack vectors based on packet size, flow duration, and protocol combinations.
