import { useEffect, useState } from "react";
import {
  MessageCircle,
  Users,
  Camera,
  BriefcaseBusiness,
  Mail,
  Music2,
  Save,
  RefreshCw,
} from "lucide-react";

import { API_URL } from "../config/api";
import WhatsAppWebPanel from "../components/WhatsAppWebPanel";

const channelMeta = {
  whatsapp: {
    label: "WhatsApp Business",
    icon: MessageCircle,
    description: "Connect WhatsApp Business and allow Jarvis to auto-reply.",
  },
  facebook: {
    label: "Facebook",
    icon: Users,
    description: "Facebook connector placeholder.",
  },
  instagram: {
    label: "Instagram",
    icon: Camera,
    description: "Instagram connector placeholder.",
  },
  linkedin: {
    label: "LinkedIn",
    icon: BriefcaseBusiness,
    description: "LinkedIn connector placeholder.",
  },
  tiktok: {
    label: "TikTok",
    icon: Music2,
    description: "TikTok connector placeholder.",
  },
  email: {
    label: "Email",
    icon: Mail,
    description: "Email connector placeholder.",
  },
};

export default function SocialChannelPanel({ channel }) {
  const meta = channelMeta[channel] || channelMeta.whatsapp;
  const Icon = meta.icon;

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [status, setStatus] = useState("");
  const [settings, setSettings] = useState({
    enabled: false,
    auto_reply: false,
    connection_mode: "web",
    phone_number_id: "",
    access_token: "",
    verify_token: "jarvis_whatsapp_verify_token",
    api_version: "v20.0",
    business_name: "LKProfessionals (Pvt) Ltd.",
    web_session_name: "default",
    web_headless: true,
  });

  useEffect(() => {
    loadSettings();
  }, [channel]);

  async function loadSettings() {
    setLoading(true);
    setStatus("");

    try {
      const response = await fetch(`${API_URL}/social/channels`);
      const data = await response.json();

      if (data.ok && data.channels?.[channel]) {
        setSettings((previous) => ({
          ...previous,
          ...data.channels[channel],
        }));
      }
    } catch {
      setStatus("Unable to connect to Jarvis API.");
    }

    setLoading(false);
  }

  function updateField(field, value) {
    setSettings((previous) => ({
      ...previous,
      [field]: value,
    }));
  }

  async function updateWhatsAppSettings(updates) {
    const nextSettings = {
      ...settings,
      ...updates,
    };

    if (updates.auto_reply === true) {
      nextSettings.enabled = true;
    }

    setSettings(nextSettings);
    setSaving(true);
    setStatus("");

    try {
      const response = await fetch(`${API_URL}/social/channels/whatsapp`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(nextSettings),
      });

      const data = await response.json();

      if (!data.ok) {
        setStatus("WhatsApp settings could not be saved.");
      }
    } catch {
      setStatus("Unable to save WhatsApp settings.");
    }

    setSaving(false);
  }

  async function saveSettings() {
    setSaving(true);
    setStatus("");

    try {
      const response = await fetch(`${API_URL}/social/channels/${channel}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(settings),
      });

      const data = await response.json();

      if (data.ok) {
        setStatus("Settings saved successfully.");
      } else {
        setStatus("Settings could not be saved.");
      }
    } catch {
      setStatus("Unable to connect to Jarvis API.");
    }

    setSaving(false);
  }

  const isWhatsApp = channel === "whatsapp";

  return (
    <section className="panel social-channel-panel">
      <div className="panel-title">
        <Icon size={26} />
        <div>
          <h2>{meta.label}</h2>
          <p>{meta.description}</p>
        </div>
      </div>

      {loading ? (
        <div className="social-loading">Loading channel settings...</div>
      ) : (
        <>
          {!isWhatsApp && (
            <div className="social-toggle-grid">
              <label className="social-toggle-card">
                <input
                  type="checkbox"
                  checked={Boolean(settings.enabled)}
                  onChange={(event) =>
                    updateField("enabled", event.target.checked)
                  }
                />
                <span>Enable Channel</span>
              </label>

              <label className="social-toggle-card">
                <input
                  type="checkbox"
                  checked={Boolean(settings.auto_reply)}
                  onChange={(event) =>
                    updateField("auto_reply", event.target.checked)
                  }
                />
                <span>Jarvis Auto Reply</span>
              </label>
            </div>
          )}

          {isWhatsApp ? (
            <WhatsAppWebPanel
              settings={settings}
              updateWhatsAppSettings={updateWhatsAppSettings}
              status={status}
              setStatus={setStatus}
            />
          ) : (
            <div className="connector-placeholder">
              <h3>{meta.label} connector is prepared.</h3>
              <p>
                The sidebar icon is active. We will connect this channel after
                WhatsApp Business auto-reply is stable.
              </p>
            </div>
          )}

          {!isWhatsApp && (
            <div className="social-actions">
              <button type="button" onClick={saveSettings} disabled={saving}>
                {saving ? <RefreshCw size={18} /> : <Save size={18} />}
                {saving ? "Saving..." : "Save Settings"}
              </button>

              <button type="button" className="secondary" onClick={loadSettings}>
                <RefreshCw size={18} />
                Reload
              </button>
            </div>
          )}

          {!isWhatsApp && status && <div className="social-status">{status}</div>}
        </>
      )}
    </section>
  );
}
