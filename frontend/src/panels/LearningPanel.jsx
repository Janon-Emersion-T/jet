import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  BookOpen,
  Pause,
  Play,
  RefreshCw,
  Sparkles,
  SquareTerminal,
  Zap,
} from "lucide-react";

import Panel from "../components/Panel";
import {
  getLearningOverview,
  runLearningCycle,
  startLearning,
  stopLearning,
} from "../services/learningService";
import { runPanelCommand } from "../services/commandService";

function StatCard({ label, value, tone = "default" }) {
  return (
    <div className={`learning-stat ${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function formatEventLabel(event) {
  return event.type || event.event_type || "event";
}

function formatEventSummary(event) {
  const payload = event.payload || {};
  if (payload.command) return payload.command;
  if (payload.message) return payload.message;
  if (payload.topic) return `${payload.topic}${payload.domain ? ` (${payload.domain})` : ""}`;
  if (payload.task?.topic) return `${payload.task.topic} (${payload.task.domain || "task"})`;
  if (event.error) return event.error;
  return JSON.stringify(payload || event, null, 0);
}

export default function LearningPanel() {
  const [overview, setOverview] = useState(null);
  const [command, setCommand] = useState("learn laravel");
  const [response, setResponse] = useState("");
  const [busy, setBusy] = useState(false);

  const domainCards = useMemo(() => overview?.domain_summaries || [], [overview]);
  const queue = useMemo(() => overview?.queue || [], [overview]);
  const events = useMemo(() => overview?.recent_events || [], [overview]);
  const stats = overview?.stats || {};

  async function loadOverview() {
    try {
      const data = await getLearningOverview(12);
      setOverview(data);
    } catch {
      setOverview(null);
    }
  }

  useEffect(() => {
    loadOverview();
    const interval = setInterval(loadOverview, 12000);
    return () => clearInterval(interval);
  }, []);

  async function handleAction(action) {
    setBusy(true);
    try {
      let result = null;

      if (action === "start") {
        result = await startLearning();
      } else if (action === "stop") {
        result = await stopLearning();
      } else if (action === "cycle") {
        result = await runLearningCycle();
      }

      if (result) {
        setResponse(
          result?.status ||
            result?.message ||
            JSON.stringify(result, null, 2)
        );
      }

      await loadOverview();
    } finally {
      setBusy(false);
    }
  }

  async function handleCommandSubmit(event) {
    event.preventDefault();
    const trimmed = command.trim();
    if (!trimmed || busy) return;

    setBusy(true);
    setResponse("");

    try {
      const data = await runPanelCommand(trimmed, "learning-panel");
      const text =
        data?.response ||
        data?.status ||
        data?.result ||
        JSON.stringify(data, null, 2);

      setResponse(text);
      await loadOverview();
    } catch (error) {
      setResponse(error.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <Panel title="Learning Studio" icon={<BookOpen />}>
      <div className="learning-shell">
        <div className="learning-header">
          <div>
            <p className="eyebrow">AUTONOMOUS MEMORY + CURRICULUM</p>
            <h2>Jarvis Learning Workspace</h2>
            <p className="learning-subtitle">
              Track what Jarvis is learning, queue new topics, and run a live learning cycle without leaving the workspace.
            </p>
          </div>

          <div className={`learning-badge ${overview?.enabled ? "live" : "paused"}`}>
            {overview?.enabled ? "Learning Active" : "Learning Paused"}
          </div>
        </div>

        <div className="learning-toolbar">
          <button onClick={loadOverview} disabled={busy}>
            <RefreshCw size={16} />
            Refresh
          </button>
          <button onClick={() => handleAction("start")} disabled={busy || overview?.enabled}>
            <Play size={16} />
            Start
          </button>
          <button onClick={() => handleAction("stop")} disabled={busy || !overview?.enabled}>
            <Pause size={16} />
            Stop
          </button>
          <button onClick={() => handleAction("cycle")} disabled={busy}>
            <Zap size={16} />
            Run Cycle
          </button>
        </div>

        <form className="learning-command-row" onSubmit={handleCommandSubmit}>
          <input
            value={command}
            onChange={(event) => setCommand(event.target.value)}
            placeholder="Ask Jarvis to learn, review, or summarize something..."
          />
          <button type="submit" disabled={busy}>
            <SquareTerminal size={16} />
            Send
          </button>
        </form>

        <div className="learning-stat-grid">
          <StatCard label="Tasks Completed" value={stats.tasks_completed ?? 0} />
          <StatCard label="Topics Learned" value={stats.topics_learned ?? 0} />
          <StatCard label="Reviews" value={stats.reviews_completed ?? 0} tone="secondary" />
          <StatCard label="Syntheses" value={stats.syntheses_completed ?? 0} tone="accent" />
          <StatCard label="Errors" value={stats.errors ?? 0} tone="danger" />
          <StatCard label="Domains" value={domainCards.length} tone="dark" />
        </div>

        <div className="learning-grid">
          <section className="panel-surface learning-card">
            <div className="mini-heading">
              <Activity size={16} />
              Domain Progress
            </div>
            <div className="learning-domain-list">
              {domainCards.length === 0 && <p>No learning domains configured yet.</p>}
              {domainCards.map((domain) => (
                <div className="learning-domain-item" key={domain.domain}>
                  <div>
                    <strong>{domain.domain}</strong>
                    <span>{domain.completed_topics} completed topics</span>
                  </div>
                  <div className="learning-domain-meta">
                    <span>Stage {domain.stage_index}</span>
                    <span>{domain.pending_tasks} pending</span>
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section className="panel-surface learning-card">
            <div className="mini-heading">
              <Sparkles size={16} />
              Queue
            </div>
            <div className="learning-queue">
              {queue.length === 0 && <p>No queued tasks right now.</p>}
              {queue.map((task) => (
                <div className="learning-event" key={task.id}>
                  <strong>{task.topic}</strong>
                  <span>
                    {task.domain} · {task.kind} · {task.status}
                  </span>
                </div>
              ))}
            </div>
          </section>
        </div>

        <div className="learning-grid">
          <section className="panel-surface learning-card">
            <div className="mini-heading">
              <BookOpen size={16} />
              Recent Learning Events
            </div>
            <div className="learning-events">
              {events.length === 0 && <p>No learning events yet.</p>}
              {events.map((event, index) => (
                <div className="learning-event" key={`${formatEventLabel(event)}-${index}`}>
                  <strong>{formatEventLabel(event)}</strong>
                  <span>{event.completed_at || event.time || event.created_at || "recent"}</span>
                  <p>{formatEventSummary(event)}</p>
                </div>
              ))}
            </div>
          </section>

          <section className="panel-surface learning-card">
            <div className="mini-heading">
              <SquareTerminal size={16} />
              Live Response
            </div>
            <div className="result-box learning-response">
              <pre>{response || overview?.status_text || "Jarvis learning status will appear here."}</pre>
            </div>
          </section>
        </div>
      </div>
    </Panel>
  );
}
