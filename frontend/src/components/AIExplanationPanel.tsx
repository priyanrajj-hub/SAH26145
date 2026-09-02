import { Alert } from '../hooks/useWebSocket';
import { ShieldAlert, Info, TrendingDown, Target } from 'lucide-react';

interface Props {
  selectedAlert: Alert | null;
}

export default function AIExplanationPanel({ selectedAlert }: Props) {
  if (!selectedAlert) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-gray-500 p-6 text-center border-2 border-dashed border-gray-800 rounded-lg">
        <Target size={48} className="mb-4 opacity-50" />
        <p>Select a flow from the live traffic table to view the AI explainability report.</p>
      </div>
    );
  }

  const { packet, analysis } = selectedAlert;

  const isMalicious = analysis.category === 'Malicious';
  const isSuspicious = analysis.category === 'Suspicious';
  const isSafe = analysis.category === 'Safe';

  return (
    <div className="space-y-6">
      {/* Overview Banner */}
      <div className={`p-4 rounded-sm border flex gap-4 ${isMalicious ? 'bg-threat-red/10 border-threat-red/30' :
          isSuspicious ? 'bg-threat-amber/10 border-threat-amber/30' :
            'bg-signal-teal/10 border-signal-teal/30'
        }`}>
        <div className={`p-2 rounded-sm h-fit ${isMalicious ? 'bg-threat-red/20 text-threat-red' :
            isSuspicious ? 'bg-threat-amber/20 text-threat-amber' :
              'bg-signal-teal/20 text-signal-teal'
          }`}>
          {isSafe ? <Info size={24} /> : <ShieldAlert size={24} />}
        </div>
        <div>
          <h3 className="font-bold text-lg mb-1">{analysis.category} Flow</h3>
          {analysis.threat_type && (
            <p className="text-sm font-medium mb-2">Threat Signature: {analysis.threat_type}</p>
          )}
          <p className="text-sm opacity-80 leading-relaxed">
            {analysis.explanation || "No explanation provided."}
          </p>
        </div>
      </div>

      {/* Confidence Score & Decay */}
      <div className="bg-gray-800/30 p-4 rounded-lg border border-gray-700/50">
        <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Model Confidence</h4>
        <div className="flex items-center gap-4">
          <div className="flex-1 h-3 bg-gray-800 rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full ${analysis.confidence > 0.8 ? 'bg-signal-teal' :
                  analysis.confidence > 0.5 ? 'bg-threat-amber' : 'bg-threat-red'
                }`}
              style={{ width: `${analysis.confidence * 100}%` }}
            ></div>
          </div>
          <span className="font-mono text-sm">{(analysis.confidence * 100).toFixed(1)}%</span>
        </div>

        {analysis.confidence < 0.6 && (
          <div className="mt-3 flex gap-2 items-start text-xs text-threat-amber/80 bg-threat-amber/10 p-2 rounded-sm border border-threat-amber/20">
            <TrendingDown size={14} className="mt-0.5 flex-shrink-0" />
            <p><strong>Confidence Decay Applied:</strong> This source IP has repeatedly exhibited similar anomalies without escalation. Threat score reduced to prevent false positive.</p>
          </div>
        )}
      </div>

      {/* Packet Details */}
      <div className="bg-gray-800/30 p-4 rounded-lg border border-gray-700/50">
        <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Extracted Features</h4>
        <dl className="grid grid-cols-2 gap-x-4 gap-y-3 text-sm">
          <div>
            <dt className="text-gray-500">Source IP</dt>
            <dd className="font-mono mt-1 text-cyan-300">{packet.source_ip}</dd>
          </div>
          <div>
            <dt className="text-gray-500">Dest Port</dt>
            <dd className="font-mono mt-1">{packet.dest_port}</dd>
          </div>
          <div>
            <dt className="text-gray-500">Protocol</dt>
            <dd className="font-mono mt-1">{packet.protocol}</dd>
          </div>
          <div>
            <dt className="text-gray-500">Flags</dt>
            <dd className="font-mono mt-1">{packet.flags}</dd>
          </div>
          <div>
            <dt className="text-gray-500">Payload Size</dt>
            <dd className="font-mono mt-1">{packet.packet_size} B</dd>
          </div>
          <div>
            <dt className="text-gray-500">Duration</dt>
            <dd className="font-mono mt-1">{packet.flow_duration.toFixed(3)} s</dd>
          </div>
        </dl>
      </div>
    </div>
  );
}
