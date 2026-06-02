import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  BookOpen,
  Pause,
  Play,
  RefreshCw,
  Search,
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
  getLearningCatalog,
  runLearningBurst,
  runLearningCycle,
  runManualLearning,
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
  if (Array.isArray(payload.topics) && payload.topics.length > 0) {
    return payload.topics.join(" · ");
  }
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

function summarizeManualResult(result) {
  if (!result) return "Manual learning completed.";

  const task = result.task || {};
  const payload = result.result || {};
  const lines = [
    result.ok ? "MANUAL LEARNING COMPLETE" : "MANUAL LEARNING STOPPED",
    [task.domain, task.kind, task.topic].filter(Boolean).join(" · "),
  ].filter(Boolean);

  if (payload.summary) {
    lines.push(payload.summary);
  } else {
    const details = [];
    if (payload.topic) details.push(`Topic: ${payload.topic}`);
    if (payload.sources_updated != null) details.push(`Sources updated: ${payload.sources_updated}`);
    if (payload.sources_skipped != null) details.push(`Sources skipped: ${payload.sources_skipped}`);
    if (payload.memory_chunks_saved != null) details.push(`Memory chunks saved: ${payload.memory_chunks_saved}`);
    if (payload.errors && payload.errors.length > 0) details.push(`Errors: ${payload.errors.join(" | ")}`);
    if (details.length > 0) {
      lines.push(details.join("\n"));
    } else {
      lines.push(JSON.stringify(payload, null, 2));
    }
  }

  if (!result.ok && result.error) {
    lines.push(`Error: ${result.error}`);
  }

  return lines.join("\n\n");
}

function buildConsoleLines(text) {
  return String(text || "")
    .split("\n")
    .map((line) => line.trimEnd())
    .filter((line) => line.length > 0);
}

function formatCatalogSubtitle(topic) {
  const parts = [];
  if (topic.category) parts.push(topic.category.replace(/-/g, " "));
  if (topic.source_count != null) parts.push(`${topic.source_count} sources`);
  return parts.join(" · ");
}

function normalizeText(value) {
  return String(value || "")
    .toLowerCase()
    .trim()
    .replace(/\s+/g, " ");
}

function buildLearningLines(overview, events) {
  const completedTopics = overview?.completed_topics || {};
  const lines = [];

  Object.entries(completedTopics).forEach(([domain, topics]) => {
    (topics || []).slice(-12).forEach((topic, index) => {
      lines.push({
        id: `${domain}-${topic}-${index}`,
        domain,
        title: topic,
        detail: "Topic learned and stored in curriculum memory.",
        status: "completed",
      });
    });
  });

  events.slice(-18).forEach((event, index) => {
    const label = formatEventLabel(event);
    const summary = formatEventSummary(event);
    lines.push({
      id: `event-${label}-${index}`,
      domain: event.domain || event.payload?.domain || "learning",
      title: label,
      detail: summary,
      status: event.type || "event",
    });
  });

  return lines.slice(-24);
}

export default function LearningPanel() {
  const [overview, setOverview] = useState(null);
  const [catalog, setCatalog] = useState([]);
  const [catalogLoading, setCatalogLoading] = useState(false);
  const [catalogQuery, setCatalogQuery] = useState("");
  const [catalogDomain, setCatalogDomain] = useState("all");
  const [selectedCatalogId, setSelectedCatalogId] = useState("");
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
  const learningLines = useMemo(
    () => buildLearningLines(overview, events),
    [overview, events]
  );
  const filteredCatalog = useMemo(() => {
    const query = normalizeText(catalogQuery);
    return catalog.filter((item) => {
      const domainMatches = catalogDomain === "all" || item.domain === catalogDomain;
      const haystack = normalizeText([
        item.topic,
        item.category,
        ...(item.aliases || []),
        ...(item.tags || []),
      ].join(" "));

      return domainMatches && (!query || haystack.includes(query));
    });
  }, [catalog, catalogDomain, catalogQuery]);
  const selectedCatalogItem = useMemo(() => {
    if (!selectedCatalogId) return null;
    return filteredCatalog.find((item) => item.id === selectedCatalogId) || null;
  }, [filteredCatalog, selectedCatalogId]);

  const consoleLines = useMemo(
    () => buildConsoleLines(response || overview?.status_text || "Jarvis learning status will appear here."),
    [response, overview]
  );

  useEffect(() => {
    autoAdvanceRef.current = autoAdvance;
  }, [autoAdvance]);

  useEffect(() => {
    busyRef.current = busy;
  }, [busy]);

  useEffect(() => {
    autoAdvancingRef.current = autoAdvancing;
  }, [autoAdvancing]);

  useEffect(() => {
    mountedRef.current = true;

    return () => {
      mountedRef.current = false;
    };
  }, []);

  useEffect(() => {
    let isMounted = true;

    async function loadCatalog() {
      setCatalogLoading(true);
      try {
        const data = await getLearningCatalog({ limit: 240 });
        if (!isMounted) return;
        setCatalog(data.topics || []);
      } catch {
        if (isMounted) {
          setCatalog([]);
        }
      } finally {
        if (isMounted) {
          setCatalogLoading(false);
        }
      }
    }

    loadCatalog();

    return () => {
      isMounted = false;
    };
  }, []);

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

  async function handleManualRun() {
    if (!selectedCatalogItem || isWorking || activeLearning) {
      return;
    }

    busyRef.current = true;
    setBusy(true);
    setResponse("");

    try {
      const data = await runManualLearning({
        domain: selectedCatalogItem.domain,
        topic: selectedCatalogItem.topic,
        kind: "learn",
        stage: selectedCatalogItem.category || "Manual Selection",
      });
      const text =
        summarizeManualResult(data) ||
        data?.status ||
        data?.message ||
        JSON.stringify(data, null, 2);

      setResponse(text);

      if (data?.overview) {
        setOverview(data.overview);
        setLastRefreshedAt(new Date().toISOString());
      } else {
        await refreshOverview({ allowAutoBurst: false });
      }
    } catch (error) {
      setResponse(error.message);
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
                Track what Jarvis is learning, queue new topics, and switch into manual mode when you want to drive a single topic yourself.
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
            <div className="learning-hero-card compact">
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

            <div className="learning-hero-card compact">
              <div className="learning-hero-label">
                <Gauge size={16} />
                Queue depth
              </div>
              <strong>{queueDepth}</strong>
              <span>{latestEvent ? formatEventLabel(latestEvent) : "Awaiting new learning signal"}</span>
            </div>

            <div className="learning-hero-card compact">
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

        <div className="learning-stat-grid learning-stat-grid-inline">
          <StatCard label="Tasks Completed" value={stats.tasks_completed ?? 0} />
          <StatCard label="Topics Learned" value={stats.topics_learned ?? 0} />
          <StatCard label="Reviews" value={stats.reviews_completed ?? 0} tone="secondary" />
          <StatCard label="Syntheses" value={stats.syntheses_completed ?? 0} tone="accent" />
          <StatCard label="Errors" value={stats.errors ?? 0} tone="danger" />
          <StatCard label="Domains" value={domainSummary.length} tone="dark" />
        </div>

        <div className="learning-workbench">
          <section className="panel-surface learning-card learning-atlas">
            <div className="learning-card-header learning-atlas-header">
              <div className="learning-card-title">
                <div className="mini-heading">
                  <Search size={16} />
                  Learning atlas
                </div>
                <p>Browse the curriculum, filter by domain, and choose exactly one topic to push manually.</p>
              </div>
              <div className="learning-atlas-controls">
                <div className="learning-search-box">
                  <Search size={14} />
                  <input
                    value={catalogQuery}
                    onChange={(event) => setCatalogQuery(event.target.value)}
                    placeholder="Search topics, aliases, or tags..."
                  />
                </div>
                <div className="learning-domain-chips">
                  {["all", "programming", "medicine"].map((domain) => (
                    <button
                      key={domain}
                      type="button"
                      className={`learning-domain-chip ${catalogDomain === domain ? "active" : ""}`}
                      onClick={() => setCatalogDomain(domain)}
                    >
                      {domain}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <div className="learning-atlas-meta">
              <span>{catalogLoading ? "Loading atlas..." : `${filteredCatalog.length} topics`}</span>
              <span>Click a topic to focus it, then press Push to learn while the engine is paused.</span>
            </div>

            <div className="learning-atlas-list learning-scroll">
              {filteredCatalog.length === 0 && (
                <div className="learning-empty-state">
                  <strong>No matching topics.</strong>
                  <span>Try a different search or switch domains.</span>
                </div>
              )}

              {filteredCatalog.map((item) => (
                <button
                  type="button"
                  key={item.id}
                  className={`learning-atlas-item ${selectedCatalogItem?.id === item.id ? "selected" : ""}`}
                  onClick={() => setSelectedCatalogId(item.id)}
                >
                  <div className="learning-atlas-item-head">
                    <strong>{item.topic}</strong>
                    <span>{item.domain}</span>
                  </div>
                  <p>{formatCatalogSubtitle(item)}</p>
                  <div className="learning-atlas-item-foot">
                    <span>{(item.aliases || []).slice(0, 3).join(" · ") || "No aliases"}</span>
                    <span>{item.source_count} sources</span>
                  </div>
                </button>
              ))}
            </div>
          </section>

          <div className="learning-right-rail">
            <section className="panel-surface learning-card learning-focus-card">
              <div className="learning-card-header">
                <div className="learning-card-title">
                  <div className="mini-heading">
                    <Sparkles size={16} />
                    Manual focus
                    <span className={`learning-live-chip ${activeLearning ? "locked" : "ready"}`}>
                      {activeLearning ? "Paused required" : "Ready"}
                    </span>
                  </div>
                  <p>Selected topic, controls, and the manual launch button live here.</p>
                </div>
                <div className="learning-card-header-actions">
                  <button
                    type="button"
                    className="learning-inline-action"
                    onClick={() => handleAction("start")}
                    disabled={isWorking || activeLearning}
                  >
                    <Play size={14} />
                    Start learning
                  </button>
                  <button
                    type="button"
                    className="learning-inline-action"
                    onClick={() => handleAction("stop")}
                    disabled={isWorking || !activeLearning}
                  >
                    <Pause size={14} />
                    Stop
                  </button>
                </div>
              </div>

              <div className="learning-focus-panel">
                <div className="learning-focus-topic">
                  <span className="learning-focus-label">Selected topic</span>
                  <strong>{selectedCatalogItem?.topic || "Select a topic from the atlas"}</strong>
                  <p>
                    {selectedCatalogItem
                      ? selectedCatalogItem.summary
                      : "The manual run button will activate when you select a topic and pause learning."}
                  </p>
                </div>

                <div className="learning-focus-grid">
                  <div className="learning-focus-stat">
                    <span>Domain</span>
                    <strong>{selectedCatalogItem?.domain || "—"}</strong>
                  </div>
                  <div className="learning-focus-stat">
                    <span>Category</span>
                    <strong>{selectedCatalogItem?.category || "—"}</strong>
                  </div>
                  <div className="learning-focus-stat">
                    <span>Sources</span>
                    <strong>{selectedCatalogItem?.source_count ?? 0}</strong>
                  </div>
                  <div className="learning-focus-stat">
                    <span>Aliases</span>
                    <strong>{selectedCatalogItem?.aliases?.length ?? 0}</strong>
                  </div>
                  <div className="learning-focus-stat">
                    <span>Target</span>
                    <strong>{selectedCatalogItem?.proficiency_target || "—"}</strong>
                  </div>
                </div>

                <div className="learning-focus-actions">
                  <button
                    type="button"
                    className="learning-manual-action"
                    onClick={handleManualRun}
                    disabled={isWorking || activeLearning || !selectedCatalogItem}
                  >
                    <Play size={16} />
                    Push to learn
                  </button>
                </div>
              </div>

              <div className="learning-queue-summary">
                <div className="learning-queue-summary-head">
                  <span>Auto queue</span>
                  <strong>{queueDepth} pending</strong>
                </div>
                <div className="learning-queue-mini learning-scroll">
                  {queue.length === 0 && (
                    <div className="learning-empty-state">
                      <strong>No queued topics right now.</strong>
                      <span>Auto learning will populate the next run when the engine advances.</span>
                    </div>
                  )}

                  {queue.map((task, index) => (
                    <div className="learning-queue-mini-item" key={task.id}>
                      <div className="learning-next-index">{String(index + 1).padStart(2, "0")}</div>
                      <div className="learning-next-copy">
                        <strong>{task.topic}</strong>
                        <span>{task.domain} · {task.kind} · {task.stage}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </section>

            <section className="panel-surface learning-card learning-live-card">
              <div className="learning-card-title">
                <div className="mini-heading">
                  <SquareTerminal size={16} />
                  Live console
                  <span className="learning-live-chip">Live</span>
                </div>
                <p>What the learning engine is doing right now, in a terminal-style feed.</p>
              </div>
              <div className="learning-live-banner learning-console">
                <SquareTerminal size={14} />
                <div className="learning-console-lines">
                  {consoleLines.map((line, index) => (
                    <div className="learning-console-line" key={`${line}-${index}`}>
                      {line}
                    </div>
                  ))}
                </div>
              </div>
              <div className="learning-events learning-scroll learning-progress-feed">
                {learningLines.length === 0 && (
                  <div className="learning-empty-state">
                    <strong>Waiting for learning activity.</strong>
                    <span>Once Jarvis processes a topic, each learned step will appear here line by line.</span>
                  </div>
                )}
                {learningLines.map((line, index) => (
                  <div className="learning-progress-line" key={line.id}>
                    <span className="learning-line-number">{String(index + 1).padStart(2, "0")}</span>
                    <div className="learning-line-copy">
                      <strong>{line.title}</strong>
                      <span>{line.domain} · {line.status}</span>
                      <p>{line.detail}</p>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </div>
        </div>
      </div>
    </Panel>
  );
}
