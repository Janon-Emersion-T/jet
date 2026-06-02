import { useEffect, useMemo, useState } from "react";
import {
  ArrowRight,
  Brain,
  Filter,
  Layers3,
  ListChecks,
  RefreshCw,
  Search,
  Shield,
  Sparkles,
  Terminal,
} from "lucide-react";
import Panel from "../components/Panel";
import { getToolRegistry } from "../services/toolsService";

function statusTone(status) {
  if (status === "active") return "active";
  if (status === "planned") return "planned";
  if (status === "not_connected") return "offline";
  return "neutral";
}

function prettyLabel(value) {
  return String(value || "")
    .replace(/[-_]/g, " ")
    .trim();
}

export default function ToolsPanel({ runCommand }) {
  const [registry, setRegistry] = useState(null);
  const [query, setQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [loading, setLoading] = useState(false);

  async function loadRegistry() {
    setLoading(true);
    try {
      const data = await getToolRegistry();
      setRegistry(data);
    } catch {
      setRegistry(null);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadRegistry();
  }, []);

  const capabilities = registry?.capabilities || [];
  const agents = registry?.agents || [];
  const quickActions = registry?.quick_actions || [];
  const departments = registry?.departments || [];
  const statusBreakdown = registry?.status_breakdown || [];

  const filteredCapabilities = useMemo(() => {
    const search = query.trim().toLowerCase();

    return capabilities.filter((capability) => {
      const matchesStatus = statusFilter === "all" || capability.status === statusFilter;
      if (!matchesStatus) return false;
      if (!search) return true;

      return (
        capability.name.toLowerCase().includes(search) ||
        capability.description.toLowerCase().includes(search) ||
        capability.status.toLowerCase().includes(search)
      );
    });
  }, [capabilities, query, statusFilter]);

  const filteredAgents = useMemo(() => {
    const search = query.trim().toLowerCase();

    return agents.filter((agent) => {
      if (!search) return true;

      const haystack = [
        agent.name,
        agent.title,
        agent.department,
        agent.objective,
        ...(agent.route_names || []),
        ...(agent.keywords || []),
        ...(agent.domains || []),
      ]
        .join(" ")
        .toLowerCase();

      return haystack.includes(search);
    });
  }, [agents, query]);

  const summary = registry?.summary || {
    capabilities: 0,
    agents: 0,
    departments: 0,
    active_capabilities: 0,
    planned_capabilities: 0,
  };

  return (
    <Panel title="Tools Control Plane" icon={<ListChecks />}>
      <div className="tools-shell">
        <div className="tools-hero">
          <div className="tools-hero-copy">
            <p className="tools-eyebrow">CAPABILITIES + SPECIALISTS</p>
            <h2>Jarvis Tool Registry</h2>
            <p className="tools-subtitle">
              A live view of what Jarvis can do, which specialists own those abilities, and the
              command shortcuts that should stay one click away.
            </p>
          </div>

          <div className={`tools-status ${loading ? "busy" : "ready"}`}>
            <Sparkles size={16} />
            {loading ? "Loading registry" : "Registry ready"}
          </div>
        </div>

        <div className="tools-metrics">
          <div className="tools-metric">
            <span>Capabilities</span>
            <strong>{summary.capabilities}</strong>
          </div>

          <div className="tools-metric">
            <span>Active</span>
            <strong>{summary.active_capabilities}</strong>
          </div>

          <div className="tools-metric">
            <span>Planned</span>
            <strong>{summary.planned_capabilities}</strong>
          </div>

          <div className="tools-metric">
            <span>Agents</span>
            <strong>{summary.agents}</strong>
          </div>
        </div>

        <div className="tools-toolbar">
          <div className="tools-search">
            <Search size={16} />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search capabilities, specialists, routes, and keywords..."
            />
          </div>

          <div className="tools-controls">
            <select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)}>
              <option value="all">All statuses</option>
              <option value="active">Active</option>
              <option value="planned">Planned</option>
              <option value="not_connected">Not connected</option>
            </select>

            <button onClick={loadRegistry} disabled={loading}>
              <RefreshCw size={16} />
              Refresh Tools
            </button>
          </div>
        </div>

        <div className="tools-command-strip">
          {quickActions.map((action) => (
            <button key={action.command} onClick={() => runCommand(action.command)}>
              <Terminal size={14} />
              <span>{action.label}</span>
              <strong>{action.command}</strong>
            </button>
          ))}
        </div>

        <div className="tools-workspace">
          <section className="tools-column">
            <div className="tools-card">
              <div className="tools-card-header">
                <div>
                  <h3>Capability Matrix</h3>
                  <p>What Jarvis can do right now, grouped by operational status.</p>
                </div>
                <span className="tools-card-chip">
                  <Filter size={12} />
                  {filteredCapabilities.length} visible
                </span>
              </div>

              <div className="tools-status-strip">
                {statusBreakdown.map((item) => (
                  <button
                    key={item.status}
                    className={`tools-status-chip ${statusFilter === item.status ? "active" : ""}`}
                    onClick={() => setStatusFilter(item.status)}
                  >
                    <span>{prettyLabel(item.status)}</span>
                    <strong>{item.count}</strong>
                  </button>
                ))}
              </div>

              <div className="tools-list">
                {filteredCapabilities.length === 0 && <p>No capabilities match this filter.</p>}

                {filteredCapabilities.map((capability) => (
                  <article key={capability.name} className={`tools-item ${statusTone(capability.status)}`}>
                    <div className="tools-item-head">
                      <strong>{prettyLabel(capability.name)}</strong>
                      <span>{prettyLabel(capability.status)}</span>
                    </div>
                    <p>{capability.description}</p>
                  </article>
                ))}
              </div>
            </div>

            <div className="tools-card">
              <div className="tools-card-header">
                <div>
                  <h3>Department Ledger</h3>
                  <p>The specialist teams behind the system.</p>
                </div>
                <span className="tools-card-chip">
                  <Layers3 size={12} />
                  {departments.length} groups
                </span>
              </div>

              <div className="tools-department-grid">
                {departments.map((item) => (
                  <div key={item.name} className="tools-department-item">
                    <span>{prettyLabel(item.name)}</span>
                    <strong>{item.count}</strong>
                  </div>
                ))}
              </div>
            </div>
          </section>

          <section className="tools-column">
            <div className="tools-card">
              <div className="tools-card-header">
                <div>
                  <h3>Specialist Atlas</h3>
                  <p>Agent objectives, route coverage, and domain expertise.</p>
                </div>
                <span className="tools-card-chip">
                  <Brain size={12} />
                  {filteredAgents.length} visible
                </span>
              </div>

              <div className="tools-list tools-list--agents">
                {filteredAgents.length === 0 && <p>No specialists match this filter.</p>}

                {filteredAgents.map((agent) => (
                  <article key={agent.key} className="tools-agent-card">
                    <div className="tools-agent-head">
                      <div>
                        <strong>{agent.name}</strong>
                        <span>{agent.title}</span>
                      </div>
                      <div className="tools-agent-meta">
                        <span>{prettyLabel(agent.department)}</span>
                        <span>{prettyLabel(agent.universe)}</span>
                      </div>
                    </div>

                    <p>{agent.objective}</p>

                    <div className="tools-chip-row">
                      {(agent.route_names || []).slice(0, 4).map((route) => (
                        <span key={route} className="tools-chip">
                          {prettyLabel(route)}
                        </span>
                      ))}
                    </div>

                    <div className="tools-agent-foot">
                      <span>{(agent.domains || []).map(prettyLabel).join(" • ")}</span>
                      {agent.safety_note ? <span>{agent.safety_note}</span> : <span>Safe by design</span>}
                    </div>
                  </article>
                ))}
              </div>
            </div>

            <div className="tools-card">
              <div className="tools-card-header">
                <div>
                  <h3>Execution Shortcuts</h3>
                  <p>Buttons that should stay one click away for day-to-day operations.</p>
                </div>
                <span className="tools-card-chip">
                  <ArrowRight size={12} />
                  Launch
                </span>
              </div>

              <div className="tools-launch-grid">
                <button onClick={() => runCommand("what can you do?")}>Capability Scan</button>
                <button onClick={() => runCommand("show memory usage")}>Memory Usage</button>
                <button onClick={() => runCommand("read error logs")}>Read Logs</button>
                <button onClick={() => runCommand("project health score")}>Health Score</button>
              </div>

              <div className="tools-note">
                <Shield size={14} />
                The Tools page should feel like an operator cockpit, not a button pile.
              </div>
            </div>
          </section>
        </div>
      </div>
    </Panel>
  );
}
