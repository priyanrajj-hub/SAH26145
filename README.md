# SIH26145 — AI-Based Detection of Cyber Threats in Unidirectional IP Traffic

**Problem Statement:** SIH26145 (NTRO) — Smart India Hackathon 2026
**Category:** Software | **Theme:** Blockchain & Cybersecurity

An AI-driven threat detection system for unidirectional (one-way, passive-tap
style) network traffic monitoring. Detects DDoS, Data Exfiltration, and
Unauthorized Tunneling patterns in real time, with an explainability layer
and confidence-decay mechanism to reduce false positives over time.

## Architecture

Synthetic unidirectional traffic (simulated flow data)
|
v
Feature extraction (packet size, flow duration, port, protocol, flags)
|
v
ML Engine: RandomForestClassifier (primary) + IsolationForest (secondary anomaly signal)
|
v
Explainability layer + Confidence-decay (reduces repeated false positives)
|
v
FastAPI backend — REST endpoints + WebSocket alert stream
|
v
React (Vite + Tailwind) dashboard — live traffic table, analytics charts, AI summary panel

## Repository structure

SAH26/
├── backend/
│ ├── main.py # FastAPI entrypoint, CORS, WebSocket routing
│ ├── requirements.txt
│ ├── api/v1/routes/
│ │ ├── traffic.py # historical logs, threat stats
│ │ └── alerts.py # alert management/filtering
│ ├── services/
│ │ ├── ml_engine.py # loads trained model, runs inference
│ │ └── websocket_manager.py # synthetic traffic generator + broadcast
│ ├── scripts/
│ │ ├── train_model.py # generates dataset, trains models
│ │ └── evaluate_model.py # precision/recall/F1/confusion matrix
│ └── models/
│ ├── schemas.py # Pydantic models
│ └── trained/ # .pkl model files (gitignored)
├── frontend/
│ ├── src/
│ │ ├── App.tsx
│ │ ├── hooks/useWebSocket.ts
│ │ └── components/
│ │ ├── Dashboard.tsx
│ │ ├── LiveTrafficTable.tsx
│ │ ├── AnalyticsCharts.tsx
│ │ └── AIExplanationPanel.tsx
│ ├── package.json
│ └── tailwind.config.js
├── docs/
│ ├── feasibility.md
│ ├── impact.md
│ ├── model_performance.md
│ └── pitch-deck-outline.md
├── .gitignore
└── README.md

## What's implemented

- Real trained ML pipeline (RandomForest + IsolationForest) on synthetic
  labeled flow data — not rule-based mocks
- Explainability layer generating plain-language reasons for each alert
- Confidence-decay logic to dampen repeated benign anomalies over time
- FastAPI backend with REST endpoints + live WebSocket alert streaming
- React dashboard: live traffic table, severity badges, analytics charts,
  AI explanation panel
- Model evaluation report with real precision/recall/F1/confusion matrix

## What's NOT implemented yet

- Real packet capture / integration with actual data-diode hardware
- Persistent database storage (currently in-memory / synthetic replay)
- Authentication / role-based access control on the dashboard
- Production-scale throughput benchmarking beyond estimates in `docs/feasibility.md`

## How to run locally

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# train the model (only needed once, or to retrain)
python scripts/train_model.py

# evaluate the model (optional, prints/saves metrics)
python scripts/evaluate_model.py

# run the API server
uvicorn main:app --reload
```

Backend runs at `http://localhost:8000`. Interactive API docs available at
`http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`. Requires **Node.js v18+**.

Once both are running, open the frontend in your browser and start the
traffic replay to see live alerts populate the dashboard.

## Documentation

- [`docs/feasibility.md`](docs/feasibility.md) — deployment feasibility on
  data-diode infrastructure, throughput estimates, Kafka scaling path
- [`docs/impact.md`](docs/impact.md) — target users, SOC analyst time
  savings, scalability reasoning
- [`docs/model_performance.md`](docs/model_performance.md) — real evaluated
  precision/recall/F1 and confusion matrix
- [`docs/pitch-deck-outline.md`](docs/pitch-deck-outline.md) — slide-ready
  outline matching SIH's standard PPT format

## Team

- Pranesh (PranesH-18-04)
- Priyanraj (priyanrajj-hub)
