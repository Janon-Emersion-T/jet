import { useState } from "react";
import {
  Bot,
  Send,
  Brain,
  Mic,
  Folder,
  Database,
  Settings,
  Activity,
} from "lucide-react";
import "./index.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [activeSection, setActiveSection] = useState("chat");
  const [messages, setMessages] = useState([
    { role: "jarvis", text: "JARVIS interface online. Awaiting your command, Janon." },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sections = [
    { id: "chat", label: "Chat", icon: Brain },
    { id: "voice", label: "Voice", icon: Mic },
    { id: "projects", label: "Projects", icon: Folder },
    { id: "memory", label: "Memory", icon: Database },
    { id: "diagnostics", label: "Diagnostics", icon: Activity },
    { id: "settings", label: "Settings", icon: Settings },
  ];

  async function sendMessage(customMessage = null) {
    const messageToSend = customMessage || input.trim();
    if (!messageToSend || loading) return;

    setMessages((prev) => [...prev, { role: "user", text: messageToSend }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: messageToSend }),
      });

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        { role: "jarvis", text: data.response || "No response received." },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { role: "jarvis", text: `Connection error: ${error.message}` },
      ]);
    }

    setLoading(false);
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  function runShortcut(command) {
    setActiveSection("chat");
    sendMessage(command);
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon"><Bot size={26} /></div>
          <div>
            <h1>JARVIS</h1>
            <p>Local AI Command System</p>
          </div>
        </div>

        <nav className="nav">
          {sections.map((section) => {
            const Icon = section.icon;
            return (
              <button
                key={section.id}
                className={activeSection === section.id ? "active" : ""}
                onClick={() => setActiveSection(section.id)}
              >
                <Icon size={18} /> {section.label}
              </button>
            );
          })}
        </nav>

        <div className="sidebar-footer">
          <span className="status-dot"></span>
          API Connected
        </div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div>
            <h2>{sections.find((s) => s.id === activeSection)?.label}</h2>
            <p>Private local AI assistant powered by Ollama + Python</p>
          </div>
          <div className="model-pill">llama3.1:8b</div>
        </header>

        {activeSection === "chat" && (
          <>
            <section className="chat-window">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`message-row ${message.role === "user" ? "user-row" : "jarvis-row"}`}
                >
                  <div className={`message ${message.role}`}>
                    <pre>{message.text}</pre>
                  </div>
                </div>
              ))}

              {loading && (
                <div className="message-row jarvis-row">
                  <div className="message jarvis"><pre>Thinking...</pre></div>
                </div>
              )}
            </section>

            <section className="input-panel">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type a command: what can you do?"
              />
              <button onClick={() => sendMessage()} disabled={loading}>
                <Send size={20} />
              </button>
            </section>
          </>
        )}

        {activeSection === "voice" && (
          <section className="content-panel">
            <h3>Voice Control</h3>
            <p>Voice mode currently runs from the Python backend terminal.</p>
            <button className="action-btn" onClick={() => runShortcut("activate voice mode")}>
              Activate Voice Mode
            </button>
          </section>
        )}

        {activeSection === "projects" && (
          <section className="content-panel">
            <h3>Projects</h3>
            <p>Inspect local projects and detect their stack.</p>
            <div className="quick-grid">
              <button onClick={() => runShortcut("list projects")}>List Projects</button>
              <button onClick={() => runShortcut("detect stack ~/Projects/downloads/Jarvis")}>Detect JARVIS Stack</button>
              <button onClick={() => runShortcut("scan project ~/Projects/downloads/Jarvis")}>Scan JARVIS Files</button>
            </div>
          </section>
        )}

        {activeSection === "memory" && (
          <section className="content-panel">
            <h3>Memory</h3>
            <p>View saved facts and search memory.</p>
            <div className="quick-grid">
              <button onClick={() => runShortcut("what do you remember")}>Show Facts</button>
              <button onClick={() => runShortcut("search memory jarvis")}>Search JARVIS Memory</button>
            </div>
          </section>
        )}

        {activeSection === "diagnostics" && (
          <section className="content-panel">
            <h3>Diagnostics</h3>
            <p>Run project health checks and AI interpretation.</p>
            <div className="quick-grid">
              <button onClick={() => runShortcut("deep check jarvis")}>Deep Check JARVIS</button>
              <button onClick={() => runShortcut("analyze project jarvis")}>Analyze JARVIS</button>
            </div>
          </section>
        )}

        {activeSection === "settings" && (
          <section className="content-panel">
            <h3>Settings</h3>
            <p>Current model: llama3.1:8b</p>
            <p>Backend: http://127.0.0.1:8000</p>
            <p>Mode: local-first, free models only</p>
          </section>
        )}
      </main>

      <aside className="system-panel">
        <h3>System Status</h3>
        <div className="status-card"><span>Backend API</span><strong>Online</strong></div>
        <div className="status-card"><span>Memory</span><strong>Active</strong></div>
        <div className="status-card"><span>Voice</span><strong>Offline</strong></div>
        <div className="status-card"><span>Browser Tools</span><strong>Active</strong></div>

        <div className="hint-box">
          <strong>Command Ideas</strong>
          <p>what can you do?</p>
          <p>list projects</p>
          <p>deep check jarvis</p>
          <p>open google</p>
        </div>
      </aside>
    </div>
  );
}

export default App;