import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  Bell,
  Clock3,
  RefreshCw,
  Search,
  ShieldAlert,
  Terminal,
} from "lucide-react";
import Panel from "../components/Panel";
import { getActivity, runPanelCommand } from "../services/commandService";
import { getActivitySummary } from "../services/logsService";

const ACTIONS = [
  { label: "Read Error Logs", command: "read error logs" },
  { label: "Analyze Laravel Logs", command: "laravel logs" },
  { label: "Session Summary", command: "coding session summary" },
  { label: "Project Health", command: "project health score" },
];

function stringifyPayload(payload) {
  if (!payload || Object.keys(payload).length === 0) {
    return "No payload.";
  }

  try {
    return JSON.stringify(payload, null, 2);
  } catch {
    return "Unable to render payload.";
  }
}

export default function LogsPanel() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState("");
  const [activity, setActivity] = useState([]);
  const [summary, setSummary] = useState(null);
  const [query, setQuery] = useState("");
  const [eventType, setEventType] = useState("all");

  async function loadActivity() {
    try {
      const [activityData, summaryData] = await Promise.all([
        getActivity(120),
        getActivitySummary(120),
      ]);

      setActivity(activityData.entries || []);
      setSummary(summaryData || null);
    } catch {
      setActivity([]);
      setSummary(null);
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

  const eventCounts = summary?.event_counts || [];

  const filteredActivity = useMemo(() => {
    const search = query.trim().toLowerCase();

    return activity.filter((entry) => {
      const matchesType = eventType === "all" || entry.event_type === eventType;
      if (!matchesType) return false;

      if (!search) return true;

      const payloadText = JSON.stringify(entry.payload || {}).toLowerCase();
      return (
        entry.event_type?.toLowerCase().includes(search) ||
        entry.time?.toLowerCase().includes(search) ||
        payloadText.includes(search)
      );
    });
  }, [activity, eventType, query]);

  return (
    <Panel title="Logs Command Center" icon={<Bell />}>
      <div className="logs-shell">
        <div className="logs-hero">
          <div className="logs-hero-copy">
            <p className="logs-eyebrow">SYSTEM ACTIVITY + COMMAND TRACE</p>
            <h2>Jarvis Log Intelligence</h2>
            <p className="logs-subtitle">
              Inspect activity at a glance, drill into command traces, and keep the operational
              trail readable enough for real debugging work.
            </p>
          </div>

          <div className={`logs-status ${loading ? "busy" : "ready"}`}>
            <Activity size={16} />
            {loading ? "Executing" : "Listening"}
          </div>
        </div>

        <div className="logs-metrics">
          <div className="logs-metric">
            <span>Events</span>
            <strong>{summary?.total ?? activity.length}</strong>
          </div>

          <div className="logs-metric">
            <span>Event types</span>
            <strong>{eventCounts.length}</strong>
          </div>

          <div className="logs-metric">
            <span>Filtered</span>
            <strong>{filteredActivity.length}</strong>
          </div>

          <div className="logs-metric">
            <span>Latest event</span>
            <strong>{summary?.latest?.event_type || "—"}</strong>
          </div>
        </div>

        <div className="logs-toolbar logs-toolbar--premium">
          <div className="logs-search">
            <Search size={16} />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Filter by event, payload, or timestamp..."
            />
          </div>

          <div className="logs-select-row">
            <select value={eventType} onChange={(event) => setEventType(event.target.value)}>
              <option value="all">All events</option>
              {eventCounts.map((item) => (
                <option key={item.event_type} value={item.event_type}>
                  {item.event_type}
                </option>
              ))}
            </select>

            <button onClick={loadActivity} disabled={loading}>
              <RefreshCw size={16} />
              Refresh Activity
            </button>
          </div>
        </div>

        <div className="logs-event-strip">
          {eventCounts.length === 0 && <p>No activity summary available yet.</p>}
          {eventCounts.map((item) => (
            <button
              key={item.event_type}
              className={`logs-event-chip ${eventType === item.event_type ? "active" : ""}`}
              onClick={() => setEventType(item.event_type)}
            >
              <span>{item.event_type}</span>
              <strong>{item.count}</strong>
            </button>
          ))}
        </div>

        <div className="logs-workspace">
          <section className="logs-card">
            <div className="logs-card-header">
              <div>
                <h3>Command Console</h3>
                <p>Run high-value diagnostics from the logs workspace.</p>
              </div>
              <span className="logs-card-chip">
                <Terminal size={12} />
                Actions
              </span>
            </div>

            <div className="logs-action-grid">
              {ACTIONS.map((action) => (
                <button
                  key={action.command}
                  onClick={() => runAction(action.command)}
                  disabled={loading}
                >
                  {action.label}
                </button>
              ))}
            </div>

            <div className="logs-result-box">
              <pre>{result || "Run a log action to inspect the result here."}</pre>
            </div>

            <div className="logs-note">
              <ShieldAlert size={14} />
              Log actions should tell you what happened, where it happened, and what to do next.
            </div>
          </section>

          <section className="logs-card">
            <div className="logs-card-header">
              <div>
                <h3>Activity Timeline</h3>
                <p>Recent events, command traces, and payload snapshots.</p>
              </div>
              <span className="logs-card-chip">
                <Clock3 size={12} />
                Live
              </span>
            </div>

            <div className="logs-list">
              {filteredActivity.length === 0 && <p>No activity logged yet.</p>}

              {filteredActivity.map((entry, index) => (
                <article key={`${entry.time}-${index}`} className="logs-item">
                  <div className="logs-item-head">
                    <strong>{entry.event_type}</strong>
                    <span>{entry.time}</span>
                  </div>
                  <pre>{stringifyPayload(entry.payload)}</pre>
                </article>
              ))}
            </div>
          </section>
        </div>
      </div>
    </Panel>
  );
}
