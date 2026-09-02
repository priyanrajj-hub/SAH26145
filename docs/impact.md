# Target Impact and SOC Efficiency

## Target User Persona
The primary users are **Security Operations Center (SOC) Analysts**, **Incident Responders**, and **Network Administrators** tasked with monitoring critical infrastructure networks that utilize unidirectional gateways.

## Quantifiable Impact & Defensible Metrics

### 1. Reduction in Manual Log Review Time (MTTR)
**The Problem:** In standard IDS environments, when a generic "Anomaly Detected" alert triggers on a unidirectional link, analysts are forced to manually pivot to raw PCAP tools (like Wireshark or Suricata logs) to figure out *why* it triggered.
**The Solution:** The **Explainability Layer** translates raw anomaly scores into precise, human-readable rationale (e.g., "Model identified unusually large payload (15420 bytes) for this protocol"). 
**Quantifiable Savings:** By eliminating the initial manual triage phase, we estimate a **60% reduction** in the time it takes an analyst to classify and prioritize an alert.

### 2. Drastic Reduction in False Positives (Alert Fatigue)
**The Problem:** Standard IDSs rely on bidirectional TCP state (SYN-ACK) to confirm threats. Without return traffic (due to the data diode), false positive rates skyrocket. Overly sensitive rules trigger constantly on benign background noise.
**The Solution:** The **Confidence-Decay Mechanism** dynamically tracks source IP behavior over time. If a specific IP generates repeated anomalies (e.g., a misconfigured backup script sending bursty UDP traffic) but the model classifies them as benign, the system actively decays the confidence score of future alerts from that IP.
**Quantifiable Savings:** This active dampening of known, non-escalating anomalies is projected to yield a **40% reduction in false positive alert volume**, directly combating SOC alert fatigue.

## Scalability and Future-Proofing
The system scales to higher traffic volumes without redesigning the core logic:
- The decoupled architecture (FastAPI backend + React frontend) allows the UI to ingest aggregated statistical summaries rather than a raw, unreadable firehose of millions of packets.
- The use of WebSockets ensures that the UI remains highly responsive. It only receives data pushed by the server when relevant, rather than wasting CPU cycles polling thousands of times per second.
