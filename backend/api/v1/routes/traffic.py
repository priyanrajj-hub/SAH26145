from fastapi import APIRouter
from typing import List
from models.schemas import ThreatSummary

router = APIRouter()

@router.get("/summary", response_model=ThreatSummary)
async def get_traffic_summary():
    # In a real application, this would query a database (e.g. TimescaleDB, ClickHouse)
    return ThreatSummary(
        total_packets=105432,
        safe_packets=104000,
        suspicious_packets=1200,
        malicious_packets=232,
        top_threat_types=["Data Exfiltration", "DDoS", "Unauthorized Tunneling"]
    )
