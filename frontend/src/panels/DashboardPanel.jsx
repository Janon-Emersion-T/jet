export default function DashboardPanel({
  apiOnline,
  facts,
  capabilities,
  runCommand,
  notify,
}) {
  return (
    <section className="panel">
      <h2>Command Center</h2>

      <p>
        Desktop shell, tray system, notifications, and React dashboard are now aligned.
      </p>

      <div className="cards">
        <div className="card">
          <strong>Backend</strong>
          <span>{apiOnline ? "Connected" : "Not connected"}</span>
        </div>

        <div className="card">
          <strong>Memory Facts</strong>
          <span>{facts.length}</span>
        </div>

        <div className="card">
          <strong>Capabilities</strong>
          <span>{capabilities.length}</span>
        </div>
      </div>

      <div className="quick-grid">
        <button onClick={() => runCommand("what can you do?")}>
          Capability Scan
        </button>

        <button onClick={() => runCommand("list projects")}>
          List Projects
        </button>

        <button onClick={() => runCommand("deep check jarvis")}>
          Deep Check
        </button>

        <button
          onClick={() =>
            notify("JARVIS Test", "Desktop notifications are working.")
          }
        >
          Test Notification
        </button>
      </div>
    </section>
  );
}
