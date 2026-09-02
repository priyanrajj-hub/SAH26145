import { useMemo } from 'react';
import { Alert } from '../hooks/useWebSocket';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  BarChart, Bar
} from 'recharts';
import { format } from 'date-fns';

interface Props {
  alerts: Alert[];
}

export default function AnalyticsCharts({ alerts }: Props) {
  // Process data for charts
  const chartData = useMemo(() => {
    // Group by minute (or 10 seconds for more lively chart in dev)
    const grouped: Record<string, { time: string, safe: number, suspicious: number, malicious: number, bandwidth: number }> = {};

    // Reverse to process chronologically
    [...alerts].reverse().forEach(alert => {
      const date = new Date(alert.packet.timestamp);
      // Group by 5 second intervals for demo purposes
      const timeKey = `${date.getHours()}:${date.getMinutes()}:${Math.floor(date.getSeconds() / 5) * 5}`;

      if (!grouped[timeKey]) {
        grouped[timeKey] = {
          time: format(date, 'HH:mm:ss'),
          safe: 0,
          suspicious: 0,
          malicious: 0,
          bandwidth: 0
        };
      }

      const cat = alert.analysis.category.toLowerCase() as 'safe' | 'suspicious' | 'malicious';
      grouped[timeKey][cat] += 1;
      grouped[timeKey].bandwidth += alert.packet.packet_size;
    });

    return Object.values(grouped).slice(-20); // Keep last 20 points
  }, [alerts]);

  if (chartData.length === 0) {
    return <div className="h-full flex items-center justify-center text-gray-500">Waiting for data...</div>;
  }

  return (
    <div className="h-[220px] w-full flex gap-4">
      {/* Threat Events Chart */}
      <div className="flex-1">
        <h4 className="text-xs text-gray-400 mb-2">Threat Events over Time</h4>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 5, right: 5, left: -20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
            <XAxis dataKey="time" stroke="#9CA3AF" fontSize={10} tickMargin={5} />
            <YAxis stroke="#9CA3AF" fontSize={10} />
            <Tooltip
              contentStyle={{ backgroundColor: '#1F2937', borderColor: '#374151', borderRadius: '8px' }}
              itemStyle={{ fontSize: '12px' }}
            />
            <Line type="monotone" dataKey="malicious" stroke="#ff5252" strokeWidth={2} dot={false} isAnimationActive={false} />
            <Line type="monotone" dataKey="suspicious" stroke="#ffda79" strokeWidth={2} dot={false} isAnimationActive={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Bandwidth Chart */}
      <div className="flex-1">
        <h4 className="text-xs text-gray-400 mb-2">Ingest Bandwidth (Bytes)</h4>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} margin={{ top: 5, right: 5, left: -10, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
            <XAxis dataKey="time" stroke="#9CA3AF" fontSize={10} tickMargin={5} />
            <YAxis stroke="#9CA3AF" fontSize={10} />
            <Tooltip
              contentStyle={{ backgroundColor: '#1F2937', borderColor: '#374151', borderRadius: '8px' }}
              itemStyle={{ fontSize: '12px' }}
              cursor={{ fill: '#374151', opacity: 0.4 }}
            />
            <Bar dataKey="bandwidth" fill="#00d2d3" radius={[2, 2, 0, 0]} isAnimationActive={false} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
