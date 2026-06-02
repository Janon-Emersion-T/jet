import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  Activity,
  BookOpen,
  Pause,
  Play,
  RefreshCw,
  Sparkles,
  SquareTerminal,
  Zap,
  WandSparkles,
  Gauge,
  Radar,
} from "lucide-react";

import Panel from "../components/Panel";
import {
  getLearningOverview,
  runLearningBurst,
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

function summarizeBurstResult(result) {
  if (!result) return "Learning burst completed.";

  const completed = result.completed_cycles ?? result?.result?.completed_cycles ?? 0;
  const requested = result.requested_cycles ?? result?.result?.requested_cycles ?? 0;
  const queueDepth = result.overview?.queue_depth ?? 0;

  return [
    "AUTONOMOUS LEARNING BURST",
    `Cycles completed: ${completed}/${requested}`,
    `Queue depth: ${queueDepth}`,
    result.status || result.overview?.status_text || "Learning state refreshed.",
  ].join("\n\n");
}

function ProgressBar({ value }) {
  const safeValue = Math.max(0, Math.min(100, Number(value) || 0));

  return (
    <div className="learning-progress">
      <div className="learning-progress-track">
        <span style={{ width: `${safeValue}%` }} />
      </div>
      <strong>{safeValue}%</strong>
    </div>
  );
}

export default function LearningPanel() {
  const [overview, setOverview] = useState(null);
  const [command, setCommand] = useState("learn laravel");
  const [response, setResponse] = useState("");
  const [busy, setBusy] = useState(false);
  const [autoAdvancing, setAutoAdvancing] = useState(false);
  const [autoAdvance, setAutoAdvance] = useState(true);
  const [lastRefreshedAt, setLastRefreshedAt] = useState("");

  const autoBurstCooldownRef = useRef(0);
  const mountedRef = useRef(true);
  const autoAdvanceRef = useRef(autoAdvance);
  const busyRef = useRef(busy);
  const autoAdvancingRef = useRef(autoAdvancing);

  const domainCards = useMemo(() => overview?.domain_summaries || [], [overview]);
  const queue = useMemo(() => overview?.queue || [], [overview]);
  const events = useMemo(() => overview?.recent_events || [], [overview]);
  const stats = overview?.stats || {};
  const queueDepth = overview?.queue_depth ?? queue.length;
  const currentTask =
    queue.find((task) => task.id === overview?.current_task_id) ||
    queue.find((task) => task.status === "in_progress") ||
    queue[0] ||
    null;
  const latestEvent = overview?.latest_event || events[events.length - 1] || null;
  const activeLearning = Boolean(overview?.enabled);
  const isWorking = busy || autoAdvancing;

  useEffect(() => {
    autoAdvanceRef.current = autoAdvance;
  }, [autoAdvance]);

  useEffect(() => {
    busyRef.current = busy;
  }, [busy]);

  useEffect(() => {
    autoAdvancingRef.current = autoAdvancing;
  }, [autoAdvancing]);

  const refreshOverview = useCallback(
    async ({ allowAutoBurst = true } = {}) => {
      try {
        const data = await getLearningOverview(12);
        if (!mountedRef.current) return data;

        setOverview(data);
        setLastRefreshedAt(new Date().toISOString());

        if (allowAutoBurst) {
          await maybeAutoAdvance(data);
        }

        return data;
      } catch {
        if (mountedRef.current) {
          setOverview(null);
        }
        return null;
      }
    },
    []
  );

  const maybeAutoAdvance = useCallback(
    async (data) => {
      if (
        !mountedRef.current ||
        !autoAdvanceRef.current ||
        busyRef.current ||
        autoAdvancingRef.current
      ) {
        return;
      }

      const depth = data?.queue_depth ?? data?.queue?.length ?? 0;
      if (!data?.enabled || depth <= 0) {
        return;
      }

      const now = Date.now();
      if (now - autoBurstCooldownRef.current < 12000) {
        return;
      }

      autoBurstCooldownRef.current = now;
      autoAdvancingRef.current = true;
      setAutoAdvancing(true);

      try {
        const burst = await runLearningBurst(3);

        if (!mountedRef.current) return;

        setResponse(summarizeBurstResult(burst?.result || burst));

        if (burst?.result?.overview) {
          setOverview(burst.result.overview);
          setLastRefreshedAt(new Date().toISOString());
          return;
        }

        await refreshOverview({ allowAutoBurst: false });
      } catch (error) {
        if (mountedRef.current) {
          setResponse(error.message);
        }
      } finally {
        if (mountedRef.current) {
          autoAdvancingRef.current = false;
          setAutoAdvancing(false);
        }
      }
    },
    [refreshOverview]
  );

  useEffect(() => {
    mountedRef.current = true;
    refreshOverview({ allowAutoBurst: true });

    const interval = setInterval(() => {
      refreshOverview({ allowAutoBurst: true });
    }, 9000);

    return () => {
      mountedRef.current = false;
      clearInterval(interval);
    };
  }, [refreshOverview]);

  async function handleAction(action) {
    busyRef.current = true;
    setBusy(true);
    try {
      let result = null;

      if (action === "start") {
        result = await startLearning();
      } else if (action === "stop") {
        result = await stopLearning();
      } else if (action === "cycle") {
        result = await runLearningCycle();
      } else if (action === "burst") {
        result = await runLearningBurst(4);
      }

      if (result) {
        setResponse(
          summarizeBurstResult(result?.result || result) ||
            result?.status ||
            result?.message ||
            JSON.stringify(result, null, 2)
        );
      }

      await refreshOverview({ allowAutoBurst: false });
    } finally {
      busyRef.current = false;
      setBusy(false);
    }
  }

  async function handleCommandSubmit(event) {
    event.preventDefault();
    const trimmed = command.trim();
    if (!trimmed || isWorking) return;

    busyRef.current = true;
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
      await refreshOverview({ allowAutoBurst: true });
    } catch (error) {
      setResponse(error.message);
    } finally {
      busyRef.current = false;
      setBusy(false);
    }
  }

  const domainSummary = domainCards.length > 0 ? domainCards : [];

  return (
    <Panel title="Learning Studio" icon={<BookOpen />}>
      <div className="learning-shell">
        <div className="learning-hero">
          <div className="learning-header">
            <div>
              <p className="eyebrow">AUTONOMOUS MEMORY + CURRICULUM</p>
              <h2>Jarvis Learning Workspace</h2>
              <p className="learning-subtitle">
                Track what Jarvis is learning, queue new topics, and let the curriculum advance automatically in the background.
              </p>
            </div>

            <div className="learning-status-stack">
              <div className={`learning-badge ${activeLearning ? "live" : "paused"}`}>
                {activeLearning ? "Learning Active" : "Learning Paused"}
              </div>
              <button
                type="button"
                className={`learning-auto-toggle ${autoAdvance ? "active" : ""}`}
                onClick={() => setAutoAdvance((value) => !value)}
                disabled={isWorking}
              >
                {autoAdvance ? "Auto Advance On" : "Auto Advance Off"}
              </button>
            </div>
          </div>

          <div className="learning-hero-grid">
            <div className="learning-hero-card">
              <div className="learning-hero-label">
                <Radar size={16} />
                Current task
              </div>
              <strong>{currentTask?.topic || "No active task"}</strong>
              <span>
                {currentTask
                  ? `${currentTask.domain} · ${currentTask.kind} · ${currentTask.status}`
                  : "Jarvis will queue the next learning task automatically."}
              </span>
            </div>

            <div className="learning-hero-card">
              <div className="learning-hero-label">
                <Gauge size={16} />
                Queue depth
              </div>
              <strong>{queueDepth}</strong>
              <span>{latestEvent ? formatEventLabel(latestEvent) : "Awaiting new learning signal"}</span>
            </div>

            <div className="learning-hero-card">
              <div className="learning-hero-label">
                <WandSparkles size={16} />
                Last refresh
              </div>
              <strong>{lastRefreshedAt ? new Date(lastRefreshedAt).toLocaleTimeString() : "Waiting"}</strong>
              <span>{overview?.last_cycle_at || "No cycle yet"}</span>
            </div>
          </div>
        </div>

        <div className="learning-toolbar">
          <button onClick={() => refreshOverview({ allowAutoBurst: false })} disabled={isWorking}>
            <RefreshCw size={16} />
            Refresh
          </button>
          <button onClick={() => handleAction("start")} disabled={isWorking || activeLearning}>
            <Play size={16} />
            Start
          </button>
          <button onClick={() => handleAction("stop")} disabled={isWorking || !activeLearning}>
            <Pause size={16} />
            Stop
          </button>
          <button onClick={() => handleAction("burst")} disabled={isWorking}>
            <Zap size={16} />
            Burst
          </button>
          <button onClick={() => handleAction("cycle")} disabled={isWorking}>
            <Sparkles size={16} />
            Run Cycle
          </button>
        </div>

        <form className="learning-command-row" onSubmit={handleCommandSubmit}>
          <input
            value={command}
            onChange={(event) => setCommand(event.target.value)}
            placeholder="Ask Jarvis to learn, review, or summarize something..."
          />
          <button type="submit" disabled={isWorking}>
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
          <StatCard label="Domains" value={domainSummary.length} tone="dark" />
        </div>

        <div className="learning-grid learning-grid-top">
          <section className="panel-surface learning-card">
            <div className="mini-heading">
              <Activity size={16} />
              Domain Progress
            </div>
            <div className="learning-domain-list learning-scroll">
              {domainSummary.length === 0 && <p>No learning domains configured yet.</p>}
              {domainSummary.map((domain) => {
                const denominator = Math.max(
                  (domain.completed_topics || 0) + (domain.pending_tasks || 0),
                  1
                );
                const completion = Math.round(((domain.completed_topics || 0) / denominator) * 100);

                return (
                  <div className="learning-domain-item" key={domain.domain}>
                    <div className="learning-domain-copy">
                      <strong>{domain.domain}</strong>
                      <span>{domain.completed_topics} completed topics</span>
                      <ProgressBar value={completion} />
                    </div>
                    <div className="learning-domain-meta">
                      <span>Stage {domain.stage_index}</span>
                      <span>{domain.pending_tasks} pending</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </section>

          <section className="panel-surface learning-card">
            <div className="mini-heading">
              <Sparkles size={16} />
              Queue
            </div>
            <div className="learning-queue learning-scroll">
              {queue.length === 0 && <p>No queued tasks right now.</p>}
              {queue.map((task) => (
                <div className="learning-event learning-event-compact" key={task.id}>
                  <strong>{task.topic}</strong>
                  <span>
                    {task.domain} · {task.kind} · {task.status}
                  </span>
                  <div className="learning-task-meta">
                    <span>{task.stage}</span>
                    <span>{task.completed_at ? "completed" : "pending"}</span>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>

        <div className="learning-grid learning-grid-bottom">
          <section className="panel-surface learning-card">
            <div className="mini-heading">
              <BookOpen size={16} />
              Recent Learning Events
            </div>
            <div className="learning-events learning-scroll">
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
