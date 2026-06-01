import { useEffect, useState } from "react";
import {
  MessageCircle,
  Facebook,
  Instagram,
  Linkedin,
  Mail,
  Music2,
  Save,
  RefreshCw,
} from "lucide-react";

const API_URL = "http://127.0.0.1:8000";

const channelMeta = {
  whatsapp: {
    label: "WhatsApp Business",
    icon: MessageCircle,
    description: "Connect WhatsApp Business and allow Jarvis to auto-reply.",
  },
  facebook: {
    label: "Facebook",
    icon: Facebook,
    description: "Facebook connector placeholder.",
  },
  instagram: {
    label: "Instagram",
    icon: Instagram,
    description: "Instagram connector placeholder.",
  },
  linkedin: {
    label: "LinkedIn",
    icon: Linkedin,
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
    phone_number_id: "",
    access_token: "",
    verify_token: "jarvis_whatsapp_verify_token",
    api_version: "v20.0",
    business_name: "LKProfessionals (Pvt) Ltd.",
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

          {isWhatsApp ? (
            <div className="social-form">
              <label>
                Business Name
                <input
                  value={settings.business_name || ""}
                  onChange={(event) =>
                    updateField("business_name", event.target.value)
                  }
                  placeholder="LKProfessionals (Pvt) Ltd."
                />
              </label>

              <label>
                WhatsApp Phone Number ID
                <input
                  value={settings.phone_number_id || ""}
                  onChange={(event) =>
                    updateField("phone_number_id", event.target.value)
                  }
                  placeholder="Meta Phone Number ID"
                />
              </label>

              <label>
                Access Token
                <textarea
                  value={settings.access_token || ""}
                  onChange={(event) =>
                    updateField("access_token", event.target.value)
                  }
                  placeholder="Meta WhatsApp Business access token"
                />
              </label>

              <label>
                Verify Token
                <input
                  value={settings.verify_token || ""}
                  onChange={(event) =>
                    updateField("verify_token", event.target.value)
                  }
                  placeholder="jarvis_whatsapp_verify_token"
                />
              </label>

              <label>
                API Version
                <input
                  value={settings.api_version || ""}
                  onChange={(event) =>
                    updateField("api_version", event.target.value)
                  }
                  placeholder="v20.0"
                />
              </label>

              <div className="webhook-card">
                <strong>Webhook Endpoint</strong>
                <code>/webhooks/whatsapp</code>
                <p>
                  When testing with ngrok, your full webhook URL will be:
                  <br />
                  <span>https://YOUR-NGROK-URL/webhooks/whatsapp</span>
                </p>
              </div>
            </div>
          ) : (
            <div className="connector-placeholder">
              <h3>{meta.label} connector is prepared.</h3>
              <p>
                The sidebar icon is active. We will connect this channel after
                WhatsApp Business auto-reply is stable.
              </p>
            </div>
          )}

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

          {status && <div className="social-status">{status}</div>}
        </>
      )}
    </section>
  );
}
