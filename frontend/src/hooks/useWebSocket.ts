import { useState, useEffect } from 'react';

export interface ThreatAnalysis {
  packet_id: string;
  threat_score: number;
  category: 'Safe' | 'Suspicious' | 'Malicious';
  threat_type?: string;
  explanation?: string;
  confidence: number;
}

export interface TrafficPacket {
  id: string;
  timestamp: string;
  source_ip: string;
  dest_ip: string;
  source_port: number;
  dest_port: number;
  protocol: string;
  packet_size: number;
  flow_duration: number;
  flags: string;
}

export interface Alert {
  id: string;
  packet: TrafficPacket;
  analysis: ThreatAnalysis;
  acknowledged: boolean;
}

export function useWebSocket(url: string) {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const ws = new WebSocket(url);

    ws.onopen = () => {
      console.log('Connected to WebSocket');
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      const data: Alert = JSON.parse(event.data);
      // Keep only the last 100 alerts to prevent memory bloat in the browser
      setAlerts((prev) => [data, ...prev].slice(0, 100));
    };

    ws.onclose = () => {
      console.log('Disconnected from WebSocket');
      setIsConnected(false);
      // Attempt reconnect after a delay (simplistic)
      setTimeout(() => setIsConnected(false), 3000); 
    };

    return () => {
      ws.close();
    };
  }, [url]);

  return { alerts, isConnected };
}
