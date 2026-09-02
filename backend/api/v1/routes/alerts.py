from fastapi import APIRouter
from typing import List

router = APIRouter()

# Mock database
alerts_db = []

@router.get("/")
async def get_alerts():
    return alerts_db

@router.post("/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: str):
    # Mock update
    return {"status": "success", "message": f"Alert {alert_id} acknowledged."}
