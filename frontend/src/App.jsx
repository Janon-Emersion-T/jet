import { useEffect, useState } from "react";
import {
  Activity,
  Bell,
  Bot,
  Brain,
  Database,
  Folder,
  Hammer,
  ListChecks,
  Mic,
  Send,
  Terminal,
  Settings,
  Cpu,
  Save,
  RefreshCw,
} from "lucide-react";
import "./index.css";

import Panel from "./components/Panel";

const API_URL = "http://127.0.0.1:8000";

const panels = [
  { id: "dashboard", label: "Dashboard", icon: Activity },
  { id: "chat", label: "Chat", icon: Brain },
  { id: "voice", label: "Voice", icon: Mic },
  { id: "projects", label: "Projects", icon: Folder },
  { id: "memory", label: "Memory", icon: Database },
  { id: "tools", label: "Tools", icon: Hammer },
  { id: "logs", label: "Logs", icon: Terminal },
  { id: "settings", label: "Settings", icon: Settings },
];

function App() {
  const [activePanel, setActivePanel] = useState("dashboard");
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [apiOnline, setApiOnline] = useState(false);
  const [facts, setFacts] = useState([]);
  const [capabilities, setCapabilities] = useState([]);
  const [messages, setMessages] = useState([
    {
      role: "jarvis",
      text: "JARVIS desktop interface online. Awaiting your command, Janon.",
    },
  ]);
  const [modelSettings, setModelSettings] = useState({});
  const [ollamaModels, setOllamaModels] = useState([]);
  const [modelTestResult, setModelTestResult] = useState("");
  const [performanceData, setPerformanceData] = useState({});
  const [promptTemplates, setPromptTemplates] = useState({});
  const [routePreview, setRoutePreview] = useState(null);
  const [routeInput, setRouteInput] = useState("");

  async function checkApi() {
    try {
      const res = await fetch(`${API_URL}/`);
      const data = await res.json();
      setApiOnline(data.status === "online");
    } catch {
      setApiOnline(false);
    }
  }

  async function loadFacts() {
    try {
      const res = await fetch(`${API_URL}/facts`);
      const data = await res.json();
      setFacts(data.facts || []);
    } catch {
      setFacts([]);
    }
  }

  async function loadCapabilities() {
    try {
      const res = await fetch(`${API_URL}/capabilities`);
      const data = await res.json();
      setCapabilities(data.capabilities || []);
    } catch {
      setCapabilities([]);
    }
  }

  async function loadModelSettings() {
    const res = await fetch(`${API_URL}/models/settings`);
    const data = await res.json();
    setModelSettings(data);
  }

  async function loadOllamaModels() {
    const res = await fetch(`${API_URL}/models/ollama`);
    const data = await res.json();
    setOllamaModels(data.models || []);
  }

  async function saveModelSettings() {
    const res = await fetch(`${API_URL}/models/settings`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(modelSettings),
    });

    const data = await res.json();
    setModelSettings(data);
    notify("JARVIS Settings Saved", "Model routing settings updated.");
  }

  async function testSelectedModel(model) {
    setModelTestResult("Testing model...");

    const res = await fetch(`${API_URL}/models/ollama/test`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model }),
    });

    const data = await res.json();
    setModelTestResult(JSON.stringify(data, null, 2));
  }

  async function loadPerformanceData() {
    const res = await fetch(`${API_URL}/models/performance`);
    const data = await res.json();
    setPerformanceData(data);
  }

  async function loadPromptTemplates() {
    const res = await fetch(`${API_URL}/prompts/templates`);
    const data = await res.json();
    setPromptTemplates(data);
  }

  async function savePromptTemplates() {
    await fetch(`${API_URL}/prompts/templates`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(promptTemplates),
    });

    notify("Prompt Templates Updated", "JARVIS templates saved.");
  }

  async function previewRoute(message) {
    const res = await fetch(`${API_URL}/models/fallback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await res.json();
    setRoutePreview(data);
  }

  useEffect(() => {
    checkApi();
    loadFacts();
    loadCapabilities();
    loadModelSettings();
    loadOllamaModels();
    loadPerformanceData();
    loadPromptTemplates();
  }, []);

  async function notify(title, body) {
    if (window.jarvisDesktop?.notify) {
      await window.jarvisDesktop.notify({ title, body });
    }
  }

  async function sendMessage(customMessage = null) {
    const message = customMessage || input.trim();
    if (!message || loading) return;

    setMessages((prev) => [...prev, { role: "user", text: message }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      const data = await res.json();
      const response = data.response || "No response received.";

      setMessages((prev) => [...prev, { role: "jarvis", text: response }]);

      if (
        message.includes("deep check") ||
        message.includes("error") ||
        message.includes("logs")
      ) {
        notify("JARVIS Task Completed", message);
      }
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { role: "jarvis", text: `Backend connection error: ${error.message}` },
      ]);
    }

    setLoading(false);
  }

  function runCommand(command) {
    setActivePanel("chat");
    sendMessage(command);
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <Bot size={30} />
          <div>
            <h1>JARVIS</h1>
            <p>Local AI Workstation</p>
          </div>
        </div>

        <nav>
          {panels.map((panel) => {
            const Icon = panel.icon;
            return (
              <button
                key={panel.id}
                className={activePanel === panel.id ? "active" : ""}
                onClick={() => setActivePanel(panel.id)}
              >
                <Icon size={18} />
                {panel.label}
              </button>
            );
          })}
        </nav>

        <div className="status-pill">
          <span className={apiOnline ? "dot online" : "dot offline"} />
          {apiOnline ? "API Online" : "API Offline"}
        </div>
      </aside>

      <main className="main-panel">
        {activePanel === "dashboard" && (
          <section className="panel">
            <h2>Command Center</h2>
            <p>Desktop shell, tray system, notifications, and React dashboard are now aligned.</p>

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
              <button onClick={() => runCommand("what can you do?")}>Capability Scan</button>
              <button onClick={() => runCommand("list projects")}>List Projects</button>
              <button onClick={() => runCommand("deep check jarvis")}>Deep Check</button>
              <button onClick={() => notify("JARVIS Test", "Desktop notifications are working.")}>
                Test Notification
              </button>
            </div>
          </section>
        )}

        {activePanel === "chat" && (
          <section className="panel chat-panel">
            <h2>Chat Panel</h2>

            <div className="messages">
              {messages.map((message, index) => (
                <div key={index} className={`message ${message.role}`}>
                  <pre>{message.text}</pre>
                </div>
              ))}
              {loading && <div className="message jarvis">Thinking...</div>}
            </div>

            <div className="composer">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type a JARVIS command..."
              />
              <button onClick={() => sendMessage()} disabled={loading}>
                <Send size={18} />
              </button>
            </div>
          </section>
        )}

        {activePanel === "voice" && (
          <Panel title="Voice Status UI" icon={<Mic />}>
            <p>Voice is still backend-terminal driven. UI can trigger the route safely.</p>
            <button onClick={() => runCommand("activate voice mode")}>Activate Voice Mode</button>
          </Panel>
        )}

        {activePanel === "projects" && (
          <Panel title="Project Panel UI" icon={<Folder />}>
            <div className="quick-grid">
              <button onClick={() => runCommand("list projects")}>List Projects</button>
              <button onClick={() => runCommand("current project")}>Current Project</button>
              <button onClick={() => runCommand("auto project")}>Auto Detect Project</button>
              <button onClick={() => runCommand("analyze project jarvis")}>Analyze JARVIS</button>
            </div>
          </Panel>
        )}

        {activePanel === "memory" && (
          <Panel title="Memory Panel UI" icon={<Database />}>
            <div className="quick-grid">
              <button onClick={() => runCommand("what do you remember")}>Show Facts</button>
              <button onClick={() => runCommand("search memory jarvis")}>Search JARVIS Memory</button>
              <button onClick={loadFacts}>Refresh Facts</button>
            </div>
          </Panel>
        )}

        {activePanel === "tools" && (
          <Panel title="Tools Panel UI" icon={<ListChecks />}>
            <div className="quick-grid">
              <button onClick={() => runCommand("git status")}>Git Status</button>
              <button onClick={() => runCommand("git diff")}>Git Diff</button>
              <button onClick={() => runCommand("inspect dependencies")}>Inspect Dependencies</button>
              <button onClick={() => runCommand("project health score")}>Health Score</button>
            </div>
          </Panel>
        )}

        {activePanel === "logs" && (
          <Panel title="Logs Panel UI" icon={<Bell />}>
            <div className="quick-grid">
              <button onClick={() => runCommand("read error logs")}>Read Error Logs</button>
              <button onClick={() => runCommand("laravel logs")}>Analyze Laravel Logs</button>
              <button onClick={() => runCommand("coding session summary")}>Session Summary</button>
            </div>
          </Panel>
        )}

        {activePanel === "settings" && (
          <Panel title="Settings & Model Routing" icon={<Settings />}>
            <p>Control JARVIS model routing without touching terminal commands.</p>

            <div className="settings-grid">
              {[
                ["general_model", "General Model"],
                ["coding_model", "Coding Model"],
                ["fast_model", "Fast Model"],
                ["long_context_model", "Long Context Model"],
                ["fallback_model", "Fallback Model"],
              ].map(([key, label]) => (
                <div className="setting-row" key={key}>
                  <label>{label}</label>
                  <select
                    value={modelSettings[key] || ""}
                    onChange={(e) =>
                      setModelSettings({
                        ...modelSettings,
                        [key]: e.target.value,
                      })
                    }
                  >
                    <option value="">Select model</option>
                    {ollamaModels.map((model) => (
                      <option key={model} value={model}>
                        {model}
                      </option>
                    ))}
                  </select>

                  <button onClick={() => testSelectedModel(modelSettings[key])}>
                    <Cpu size={16} />
                    Test
                  </button>
                </div>
              ))}
            </div>

            <div className="quick-grid">
              <button onClick={loadOllamaModels}>
                <RefreshCw size={16} />
                Refresh Models
              </button>

              <button onClick={saveModelSettings}>
                <Save size={16} />
                Save Settings
              </button>
            </div>

            <hr className="separator" />

            <h3>Model Performance Monitor</h3>

            <div className="performance-grid">
              {Object.values(performanceData).map((item) => (
                <div className="performance-card" key={item.model}>
                  <strong>{item.model}</strong>

                  <span>
                    Status: {item.ok ? "ONLINE" : "FAILED"}
                  </span>

                  <span>
                    Latency: {item.latency_seconds}s
                  </span>

                  <button
                    onClick={async () => {
                      await fetch(`${API_URL}/models/performance/test`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ model: item.model }),
                      });

                      loadPerformanceData();
                    }}
                  >
                    Retest
                  </button>
                </div>
              ))}
            </div>

            <hr className="separator" />

            <h3>Fallback Route Inspector</h3>

            <div className="route-box">
              <textarea
                placeholder="Type a message to inspect model routing..."
                value={routeInput}
                onChange={(e) => setRouteInput(e.target.value)}
              />

              <button onClick={() => previewRoute(routeInput)}>
                Preview Route
              </button>

              {routePreview && (
                <pre className="route-preview">
                  {JSON.stringify(routePreview, null, 2)}
                </pre>
              )}
            </div>

            <hr className="separator" />

            <h3>Prompt Template Manager</h3>

            <div className="template-grid">
              {Object.entries(promptTemplates).map(([key, value]) => (
                <div className="template-card" key={key}>
                  <label>{key}</label>

                  <textarea
                    value={value}
                    onChange={(e) =>
                      setPromptTemplates({
                        ...promptTemplates,
                        [key]: e.target.value,
                      })
                    }
                  />
                </div>
              ))}
            </div>

            <button onClick={savePromptTemplates}>
              Save Prompt Templates
            </button>

            {modelTestResult && (
              <div className="log-box">
                <pre>{modelTestResult}</pre>
              </div>
            )}
          </Panel>
        )}
      </main>
    </div>
  );
}

export default App;