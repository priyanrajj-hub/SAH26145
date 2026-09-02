import asyncio
import json
import random
import uuid
from datetime import datetime
from fastapi import WebSocket
from typing import List, Dict

from models.schemas import TrafficPacket, ThreatAnalysis, Alert
from services.ml_engine import ml_engine

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Failed to send message: {e}")

manager = ConnectionManager()

def generate_mock_packet() -> dict:
    """Simulates unidirectional network traffic (e.g., from a data diode)"""
    ips = [f"192.168.1.{random.randint(1, 255)}" for _ in range(5)]
    ips.append(f"10.0.0.{random.randint(1, 255)}") # external
    
    source_ip = random.choice(ips)
    dest_ip = "192.168.1.100" # Internal server
    
    protocols = ["TCP", "UDP", "ICMP"]
    protocol = random.choices(protocols, weights=[0.7, 0.2, 0.1])[0]
    
    packet_size = random.randint(40, 1500)
    # Introduce anomalies randomly
    if random.random() < 0.05:
        packet_size = random.randint(1500, 65000)
        
    flow_duration = random.uniform(0.001, 5.0)
    if random.random() < 0.05:
        flow_duration = random.uniform(10.0, 30.0)
        
    return {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "source_ip": source_ip,
        "dest_ip": dest_ip,
        "source_port": random.randint(1024, 65535),
        "dest_port": random.choice([80, 443, 22, 53, 3306]),
        "protocol": protocol,
        "packet_size": packet_size,
        "flow_duration": flow_duration,
        "flags": random.choice(["ACK", "SYN", "FIN", "RST", "PSH,ACK"])
    }

async def traffic_generator():
    """Background task to generate traffic and stream alerts."""
    while True:
        packet_dict = generate_mock_packet()
        
        # Analyze packet through ML Engine
        threat_score, category, threat_type, explanation, confidence = ml_engine.analyze_packet(packet_dict)
        
        packet_obj = TrafficPacket(**packet_dict)
        analysis_obj = ThreatAnalysis(
            packet_id=packet_dict['id'],
            threat_score=threat_score,
            category=category,
            threat_type=threat_type,
            explanation=explanation,
            confidence=confidence
        )
        
        alert_obj = Alert(
            id=str(uuid.uuid4()),
            packet=packet_obj,
            analysis=analysis_obj,
            acknowledged=False
        )
        
        # Broadcast all traffic to the UI so we can see the live feed
        # In a real scenario, we might only broadcast Malicious/Suspicious or 
        # send normal traffic at a sampled rate.
        await manager.broadcast(alert_obj.model_dump_json())
        
        await asyncio.sleep(random.uniform(0.2, 1.5))
