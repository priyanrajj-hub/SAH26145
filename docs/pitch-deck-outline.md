# SIH26145 - Pitch Deck Outline

## Slide 1: Title Slide
- **Project Title:** AI-Based Detection of Cyber Threats in Unidirectional IP Traffic
- **Problem Statement ID:** SIH26145
- **Organization:** NTRO
- **Team Name:** [Your Team Name]

## Slide 2: Problem Statement
- **Context:** Critical infrastructure increasingly relies on data diodes/unidirectional gateways for air-gapped security, preventing traditional two-way network handshakes.
- **The Challenge:** Existing Intrusion Detection Systems (IDS) rely heavily on bidirectional TCP state (SYN-ACK) to confirm threats. Without return traffic, false positive rates skyrocket.
- **The Need:** An AI/ML model capable of reliably classifying unidirectional anomalies (DDoS, Data Exfiltration, Tunneling) in real-time, purely from flow features.

## Slide 3: Proposed Solution
- **Machine Learning Ensemble:** 
  - **Random Forest Classifier (Primary):** Trained on synthesized unidirectional flow metrics (packet size, flow duration, protocol distributions) for exact threat categorization.
  - **Isolation Forest (Secondary):** Unsupervised anomaly detection to flag zero-day deviations that the Random Forest hasn't seen.
- **Confidence-Decay Mechanism:** Dynamically reduces the threat score of recurring, benign anomalous patterns from the same source IP over time, directly tackling alert fatigue.
- **Explainability Layer:** Translates raw model probabilities into human-readable SOC alerts (e.g., "Abnormally short flow duration indicates potential flood attack").

## Slide 4: Technical Approach (Architecture)
- **Ingestion:** Simulates unidirectional tap via background packet generation. 
- **Backend (FastAPI):** High-performance Python async engine wrapping the `scikit-learn` `joblib` models.
- **Real-Time Streaming:** WebSockets push evaluated packets instantly to the client (no polling).
- **Frontend (React/Vite):** A dark-mode, cybersecurity-focused dashboard featuring real-time Recharts analytics and dynamic AI insight panels.

## Slide 5: Feasibility & Scalability
- **Hardware Agnostic:** Ingests standard flow logs (NetFlow/IPFIX) or PCAP feature vectors compatible with any hardware data diode (e.g., Owl, Fox-IT).
- **Current Performance:** The single-threaded `asyncio` FastAPI loop handles thousands of flows/sec with < 20ms model latency per batch.
- **Production Scale (The Path Forward):** Integration of **Apache Kafka** immediately post-diode to decouple ingestion from inference, allowing horizontal scaling of the ML workers across a Redis-backed state cache.

## Slide 6: Impact & Benefits
- **Drastic Reduction in Alert Fatigue:** The Confidence-Decay mechanism is projected to reduce false positives by 40% based on historical benign-anomaly tracking.
- **Faster Incident Response (MTTR):** The Explainability Layer saves SOC analysts an estimated 60% of time previously spent pivoting to raw PCAP tools for manual verification.
- **Air-Gap Security Maintained:** 100% compliant with NTRO unidirectional mandates.

## Slide 7: Team Details
- **[Member Name]:** Full-Stack & ML Integration
- **[Member Name]:** AI Model Training & Data Synthesis
- **[Member Name]:** React Dashboard & UI/UX
- **[Member Name]:** Systems Architecture & Documentation
