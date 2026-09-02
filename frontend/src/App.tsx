import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="min-h-screen bg-gray-950 text-gray-200 selection:bg-cyan-500/30">
      <header className="border-b border-gray-800 bg-gray-900/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-sm bg-signal-teal/20 border border-signal-teal/50 flex items-center justify-center text-signal-teal font-bold font-mono">
              NT
            </div>
            <h1 className="text-xl font-semibold tracking-tight font-sans">NTRO ThreatSense</h1>
          </div>
          <div className="flex items-center gap-4 text-sm text-gray-400 font-mono">
            <span>Unidirectional Gateway: <span className="text-signal-teal font-bold">Online</span></span>
            <span>|</span>
            <span>AI Inference Engine: <span className="text-signal-teal font-bold">Active</span></span>
          </div>
        </div>
        {/* Flow indicator bar */}
        <div className="h-[2px] w-full bg-gray-800 overflow-hidden">
          <div className="h-full w-1/3 bg-gradient-to-r from-transparent via-signal-teal to-transparent animate-flow"></div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
