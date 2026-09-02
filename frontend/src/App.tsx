import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="min-h-screen bg-gray-950 text-gray-200 selection:bg-cyan-500/30">
      <header className="border-b border-gray-800 bg-gray-900/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded bg-cyan-500/20 border border-cyan-500/50 flex items-center justify-center text-cyan-400 font-bold">
              NT
            </div>
            <h1 className="text-xl font-semibold tracking-tight">NTRO ThreatSense</h1>
          </div>
          <div className="flex items-center gap-4 text-sm text-gray-400">
            <span>Unidirectional Gateway: <span className="text-emerald-400">Online</span></span>
            <span>|</span>
            <span>AI Inference Engine: <span className="text-emerald-400">Active</span></span>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
