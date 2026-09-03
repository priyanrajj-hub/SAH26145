# ML Model Performance Evaluation

This document contains the evaluation metrics for the supervised `RandomForestClassifier` trained on the synthetic flow dataset.

## Overall Metrics
- **Precision (weighted):** 0.9025
- **Recall (weighted):** 0.9030
- **F1-Score (weighted):** 0.9021

## Classification Report
```text
                   precision    recall  f1-score   support

             Safe       0.91      0.95      0.93      1198
             DDoS       0.91      0.88      0.90       415
Data Exfiltration       0.95      0.85      0.90       212
        Tunneling       0.78      0.72      0.75       175

         accuracy                           0.90      2000
        macro avg       0.89      0.85      0.87      2000
     weighted avg       0.90      0.90      0.90      2000

```

## Confusion Matrix
Rows are actual labels, columns are predicted labels in order: Safe, DDoS, Data Exfiltration, Tunneling.
```text
[[1133   37    8   20]
 [  47  367    0    1]
 [  17    1  180   14]
 [  47    0    2  126]]
```

## Methodology
The model was evaluated on a 20% held-out test split of 10,000 synthetic records. The high accuracy indicates the Random Forest successfully learned the distinct boundaries between our simulated attack vectors based on packet size, flow duration, and protocol combinations.
