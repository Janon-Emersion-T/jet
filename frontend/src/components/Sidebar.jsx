import {
  Power,
  MessageCircle,
  Users,
  Camera,
  BriefcaseBusiness,
  Mail,
  Music2,
} from "lucide-react";

import StatusPill from "./StatusPill";
import { panels } from "../data/panels";

const socialChannels = [
  { id: "whatsapp", label: "WhatsApp", icon: MessageCircle },
  { id: "facebook", label: "Facebook", icon: Users },
  { id: "instagram", label: "Instagram", icon: Camera },
  { id: "linkedin", label: "LinkedIn", icon: BriefcaseBusiness },
  { id: "tiktok", label: "TikTok", icon: Music2 },
  { id: "email", label: "Email", icon: Mail },
];

export default function Sidebar({ activePanel, setActivePanel, apiOnline, voiceEnabled, onToggleVoice }) {
  async function closeJarvis() {
    if (window.jarvisDesktop?.quitApp) {
      await window.jarvisDesktop.quitApp();
    }
  }

  return (
    <aside className="sidebar">
      <div className="brand">
        <button
          type="button"
          className={`voice-toggle ${voiceEnabled ? "active" : ""}`}
          onClick={onToggleVoice}
          title={voiceEnabled ? "Voice mode active" : "Activate voice mode"}
        >
          {voiceEnabled ? "Voice On" : "Voice"}
        </button>
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
