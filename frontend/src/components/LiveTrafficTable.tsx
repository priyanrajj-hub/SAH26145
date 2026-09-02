import { Alert } from '../hooks/useWebSocket';
import { format } from 'date-fns';
import { AlertTriangle, ShieldCheck, HelpCircle } from 'lucide-react';

interface Props {
  alerts: Alert[];
  onSelectRow: (alert: Alert) => void;
  selectedId?: string;
}

export default function LiveTrafficTable({ alerts, onSelectRow, selectedId }: Props) {
  if (alerts.length === 0) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-gray-500">
        <div className="animate-pulse flex space-x-4">
          <div className="h-2 bg-gray-700 rounded w-24"></div>
          <div className="h-2 bg-gray-700 rounded w-24"></div>
        </div>
        <p className="mt-4">Listening for unidirectional traffic...</p>
      </div>
    );
  }

  return (
    <div className="overflow-auto h-full pr-2">
      <table className="w-full text-sm text-left">
        <thead className="text-xs text-gray-400 uppercase bg-gray-800/50 sticky top-0 z-10">
          <tr>
            <th className="px-4 py-3">Time</th>
            <th className="px-4 py-3">Source IP</th>
            <th className="px-4 py-3">Dest Port</th>
            <th className="px-4 py-3">Protocol</th>
            <th className="px-4 py-3">Size (B)</th>
            <th className="px-4 py-3">Status</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-800/50">
          {alerts.map((alert) => {
            const isMalicious = alert.analysis.category === 'Malicious';
            const isSuspicious = alert.analysis.category === 'Suspicious';
            const isSafe = alert.analysis.category === 'Safe';

            let rowClass = 'hover:bg-gray-800/50 cursor-pointer transition-colors';
            if (alert.id === selectedId) {
              rowClass += ' bg-gray-800/80 ring-1 ring-inset ring-gray-600';
            }
            if (isMalicious) rowClass += ' border-l-2 border-red-500';
            else if (isSuspicious) rowClass += ' border-l-2 border-yellow-500';
            else rowClass += ' border-l-2 border-transparent';

            return (
              <tr 
                key={alert.id} 
                className={rowClass}
                onClick={() => onSelectRow(alert)}
              >
                <td className="px-4 py-3 text-gray-400 font-mono text-xs">
                  {format(new Date(alert.packet.timestamp), 'HH:mm:ss.SSS')}
                </td>
                <td className="px-4 py-3 font-mono">{alert.packet.source_ip}</td>
                <td className="px-4 py-3 font-mono">{alert.packet.dest_port}</td>
                <td className="px-4 py-3">{alert.packet.protocol}</td>
                <td className="px-4 py-3">{alert.packet.packet_size}</td>
                <td className="px-4 py-3">
                  {isMalicious && <span className="inline-flex items-center gap-1.5 px-2 py-1 rounded bg-red-500/10 text-red-400 border border-red-500/20"><AlertTriangle size={14} /> Malicious</span>}
                  {isSuspicious && <span className="inline-flex items-center gap-1.5 px-2 py-1 rounded bg-yellow-500/10 text-yellow-400 border border-yellow-500/20"><HelpCircle size={14} /> Suspicious</span>}
                  {isSafe && <span className="inline-flex items-center gap-1.5 px-2 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"><ShieldCheck size={14} /> Safe</span>}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
