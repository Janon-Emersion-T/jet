import { Cpu, RefreshCw, Save, Settings } from "lucide-react";
import Panel from "../components/Panel";

export default function SettingsPanel({
  modelSettings,
  setModelSettings,
  ollamaModels,
  modelTestResult,
  performanceData,
  promptTemplates,
  setPromptTemplates,
  routeInput,
  setRouteInput,
  routePreview,
  loadOllamaModels,
  saveModelSettings,
  testSelectedModel,
  testPerformance,
  previewRoute,
  savePromptTemplates,
}) {
  return (
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

      {modelTestResult && (
        <div className="log-box">
          <pre>{modelTestResult}</pre>
        </div>
      )}

      <hr className="separator" />

      <h3>Model Performance Monitor</h3>

      <div className="performance-grid">
        {Object.values(performanceData).map((item) => (
          <div className="performance-card" key={item.model}>
            <strong>{item.model}</strong>
            <span>Status: {item.ok ? "ONLINE" : "FAILED"}</span>
            <span>Latency: {item.latency_seconds}s</span>

            <button onClick={() => testPerformance(item.model)}>
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
    </Panel>
  );
}
