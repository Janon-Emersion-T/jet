import { Brain, MessageSquare, Cpu, Zap } from "lucide-react";

export default function ChatContextPanel({ messages, apiOnline, activePanel }) {
  const lastMessages = messages.slice(-5);

  return (
    <aside className="context-panel">
      <div className="jarvis-orb">
        <div className="orb-ring"></div>
        <img src="/logo.png" className="jarvis-logo-core" alt="JARVIS" />
      </div>

      <div className="context-title">
        <Brain size={20} />
        <div>
          <h2>JARVIS Context</h2>
          <p>{apiOnline ? "Neural link active" : "API connection offline"}</p>
        </div>
      </div>

      <div className="context-card">
        <span>Active Module</span>
        <strong>{activePanel}</strong>
      </div>

      <div className="context-card">
        <span>System State</span>
        <strong>{apiOnline ? "ONLINE" : "OFFLINE"}</strong>
      </div>

      <div className="context-feed">
        <div className="mini-heading">
          <MessageSquare size={16} />
          Recent Context
        </div>

        {lastMessages.map((msg, index) => (
          <div key={index} className={`context-message ${msg.role}`}>
            {msg.text.slice(0, 120)}
          </div>
        ))}
      </div>

      <div className="context-footer">
        <Cpu size={16} />
        <span>Local AI Workstation</span>
        <Zap size={16} />
      </div>
    </aside>
  );
}
