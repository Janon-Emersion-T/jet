import {
  Bot,
  Power,
  MessageCircle,
  Facebook,
  Instagram,
  Linkedin,
  Mail,
  Music2,
} from "lucide-react";

import StatusPill from "./StatusPill";
import { panels } from "../data/panels";

const socialChannels = [
  { id: "whatsapp", label: "WhatsApp", icon: MessageCircle },
  { id: "facebook", label: "Facebook", icon: Facebook },
  { id: "instagram", label: "Instagram", icon: Instagram },
  { id: "linkedin", label: "LinkedIn", icon: Linkedin },
  { id: "tiktok", label: "TikTok", icon: Music2 },
  { id: "email", label: "Email", icon: Mail },
];

export default function Sidebar({ activePanel, setActivePanel, apiOnline }) {
  async function closeJarvis() {
    if (window.jarvisDesktop?.quitApp) {
      await window.jarvisDesktop.quitApp();
    }
  }

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

        <div className="social-nav-block">
          {socialChannels.map((channel) => {
            const Icon = channel.icon;

            return (
              <button
                key={channel.id}
                type="button"
                className={`social-nav-icon ${
                  activePanel === channel.id ? "active" : ""
                }`}
                title={channel.label}
                onClick={() => setActivePanel(channel.id)}
              >
                <Icon size={18} />
              </button>
            );
          })}
        </div>

        <button className="danger-nav" onClick={closeJarvis}>
          <Power size={18} />
          Close JARVIS
        </button>
      </nav>

      <StatusPill online={apiOnline} />
    </aside>
  );
}