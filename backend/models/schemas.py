from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TrafficPacket(BaseModel):
    id: str
    timestamp: datetime
    source_ip: str
    dest_ip: str
    source_port: int
    dest_port: int
    protocol: str
    packet_size: int
    flow_duration: float
    flags: str

class ThreatAnalysis(BaseModel):
    packet_id: str
    threat_score: float
    category: str # "Safe", "Suspicious", "Malicious"
    threat_type: Optional[str] = None # e.g., "DDoS", "Data Exfiltration"
    explanation: Optional[str] = None # Explainability layer
    confidence: float # Confidence of the prediction

class Alert(BaseModel):
    id: str
    packet: TrafficPacket
    analysis: ThreatAnalysis
    acknowledged: bool = False

class ThreatSummary(BaseModel):
    total_packets: int
    safe_packets: int
    suspicious_packets: int
    malicious_packets: int
    top_threat_types: List[str]
