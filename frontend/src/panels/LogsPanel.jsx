import { useEffect, useState } from "react";
import { Bell, RefreshCw } from "lucide-react";
import Panel from "../components/Panel";
import { getActivity, runPanelCommand } from "../services/commandService";


const ACTIONS = [
  { label: "Read Error Logs", command: "read error logs" },
  { label: "Analyze Laravel Logs", command: "laravel logs" },
  { label: "Session Summary", command: "coding session summary" },
];


export default function LogsPanel() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState("");
  const [activity, setActivity] = useState([]);

  async function loadActivity() {
    try {
      const data = await getActivity(60);
      setActivity(data.entries || []);
    } catch {
      setActivity([]);
    }
  }

  async function runAction(command) {
    setLoading(true);
    try {
      const data = await runPanelCommand(command, "logs-panel");
      setResult(data.response || "No response received.");
      await loadActivity();
    } catch (error) {
      setResult(`Failed to run command: ${error.message}`);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadActivity();
  }, []);

  return (
    <Panel title="Logs Console" icon={<Bell />}>
      <div className="quick-grid">
        {ACTIONS.map((action) => (
          <button
            key={action.command}
            onClick={() => runAction(action.command)}
            disabled={loading}
          >
            {action.label}
          </button>
        ))}

        <button onClick={loadActivity} disabled={loading}>
          <RefreshCw size={16} />
          Refresh Activity
        </button>
      </div>

      <div className="logs-layout">
        <section className="panel-surface">
          <h3>Result</h3>
          <div className="result-box">
            <pre>{result || "Run a log action to inspect the result here."}</pre>
          </div>
        </section>

        <section className="panel-surface">
          <h3>Activity Log</h3>
          <div className="activity-list">
            {activity.length === 0 && <p>No activity logged yet.</p>}

            {activity.map((entry, index) => (
              <div key={`${entry.time}-${index}`} className="activity-item">
                <strong>{entry.event_type}</strong>
                <span>{entry.time}</span>
                <pre>{JSON.stringify(entry.payload || {}, null, 2)}</pre>
              </div>
            ))}
          </div>
        </section>
      </div>
    </Panel>
  );
}
