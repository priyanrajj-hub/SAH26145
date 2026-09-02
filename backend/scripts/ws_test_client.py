import asyncio
import websockets
import json

async def test_ws():
    uri = "ws://localhost:8000/ws/traffic"
    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected! Listening for packets...")
            for i in range(5):
                message = await websocket.recv()
                alert = json.loads(message)
                analysis = alert.get("analysis", {})
                packet = alert.get("packet", {})
                
                print(f"\n--- Packet {i+1} ---")
                print(f"Flow: {packet.get('source_ip')} -> {packet.get('dest_ip')}:{packet.get('dest_port')} ({packet.get('protocol')})")
                print(f"Size: {packet.get('packet_size')}B | Duration: {packet.get('flow_duration'):.3f}s")
                print(f"Prediction: {analysis.get('category')} ({analysis.get('threat_type')})")
                print(f"Threat Score (Confidence): {analysis.get('threat_score'):.4f} (Base: {analysis.get('confidence'):.4f})")
                print(f"Explanation: {analysis.get('explanation')}")
                
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_ws())
