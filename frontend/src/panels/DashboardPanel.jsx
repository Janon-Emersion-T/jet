import { Activity, Cpu, Database, Radar, Shield, Zap } from "lucide-react";

export default function DashboardPanel({
  apiOnline,
  facts,
  capabilities,
  runCommand,
  notify,
}) {
  return (
    <section className="panel jarvis-dashboard">
      <div className="panel-body">
        <div className="holo-header">
          <div>
            <p className="eyebrow">LOCAL AI WORKSTATION</p>
            <h2>JARVIS Neural Command Interface</h2>
            <p className="holo-subtitle">
              Systems, memory, tools, diagnostics, and command intelligence are standing by.
            </p>
          </div>

          <div className={`system-badge ${apiOnline ? "live" : "dead"}`}>
            <span></span>
            {apiOnline ? "CORE ONLINE" : "CORE OFFLINE"}
          </div>
        </div>

        <div className="jarvis-holo-grid">
          <div className="holo-orb-large">
            <div className="scan-ring ring-one"></div>
            <div className="scan-ring ring-two"></div>
            <div className="scan-ring ring-three"></div>
            <img src="/logo.png" alt="JARVIS" />
          </div>

          <div className="holo-stats">
            <div className="holo-stat">
              <Cpu size={22} />
              <span>Backend</span>
              <strong>{apiOnline ? "Connected" : "Not connected"}</strong>
            </div>

            <div className="holo-stat">
              <Database size={22} />
              <span>Memory Facts</span>
              <strong>{facts.length}</strong>
            </div>

            <div className="holo-stat">
              <Radar size={22} />
              <span>Capabilities</span>
              <strong>{capabilities.length}</strong>
            </div>
          </div>
        </div>

        <div className="jarvis-actions">
          <button onClick={() => runCommand("what can you do?")}>
            <Activity size={18} />
            Capability Scan
          </button>

          <button onClick={() => runCommand("list projects")}>
            <Radar size={18} />
            Project Matrix
          </button>

          <button onClick={() => runCommand("deep check jarvis")}>
            <Shield size={18} />
            Deep System Check
          </button>

          <button onClick={() => notify("JARVIS Test", "Desktop notifications are working.")}>
            <Zap size={18} />
            Test Notification
          </button>
        </div>
      </div>
    </section>
  );
}
