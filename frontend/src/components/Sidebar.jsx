import { Bot } from "lucide-react";
import StatusPill from "./StatusPill";
import { panels } from "../data/panels";

export default function Sidebar({ activePanel, setActivePanel, apiOnline }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <img src="/icon.png" className="brand-icon" alt="JARVIS" />
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

      <StatusPill online={apiOnline} />
    </aside>
  );
}
