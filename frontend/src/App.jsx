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
import {
  getModelSettings,
  saveModelSettingsRequest,
  getOllamaModels,
  testOllamaModel,
  getModelPerformance,
  testModelPerformance,
  getModelFallback,
  getPromptTemplates,
  savePromptTemplatesRequest,
} from "./services/modelService";

import Panel from "./components/Panel";

import SettingsPanel from "./panels/SettingsPanel";
import Sidebar from "./components/Sidebar";

import { sendChatMessage } from "./services/chatService";
import { checkApiStatus, getCapabilities } from "./services/systemService";
import { getFacts } from "./services/memoryService";

import ChatPanel from "./panels/ChatPanel";

import DashboardPanel from "./panels/DashboardPanel";

import VoicePanel from "./panels/VoicePanel";
import ProjectPanel from "./panels/ProjectPanel";
import MemoryPanel from "./panels/MemoryPanel";
import ToolsPanel from "./panels/ToolsPanel";
import LogsPanel from "./panels/LogsPanel";

const API_URL = "http://127.0.0.1:8000";

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
      const data = await checkApiStatus();
      setApiOnline(data.status === "online");
    } catch {
      setApiOnline(false);
    }
  }

  async function loadFacts() {
    try {
      const data = await getFacts();
      setFacts(data.facts || []);
    } catch {
      setFacts([]);
    }
  }

  async function loadCapabilities() {
    try {
      const data = await getCapabilities();
      setCapabilities(data.capabilities || []);
    } catch {
      setCapabilities([]);
    }
  }

  async function loadModelSettings() {
    const data = await getModelSettings();
    setModelSettings(data);
  }

  async function loadOllamaModels() {
    const data = await getOllamaModels();
    setOllamaModels(data.models || []);
  }

  async function saveModelSettings() {
    const data = await saveModelSettingsRequest(modelSettings);
    setModelSettings(data);
    notify("JARVIS Settings Saved", "Model routing settings updated.");
  }

  async function testSelectedModel(model) {
    setModelTestResult("Testing model...");

    const data = await testOllamaModel(model);
    setModelTestResult(JSON.stringify(data, null, 2));
  }

  async function loadPerformanceData() {
    const data = await getModelPerformance();
    setPerformanceData(data);
  }

  async function testPerformance(model) {
    await testModelPerformance(model);
    loadPerformanceData();
  }

  async function loadPromptTemplates() {
    const data = await getPromptTemplates();
    setPromptTemplates(data);
  }

  async function savePromptTemplates() {
    await savePromptTemplatesRequest(promptTemplates);
    notify("Prompt Templates Updated", "JARVIS templates saved.");
  }

  async function previewRoute(message) {
    const data = await getModelFallback(message);
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
      const data = await sendChatMessage(message);
      const response = data.response || "No response received.";

      setMessages((prev) => [
        ...prev,
        { role: "jarvis", text: response },
      ]);

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
        {
          role: "jarvis",
          text: `Backend connection error: ${error.message}`,
        },
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
      <Sidebar
        activePanel={activePanel}
        setActivePanel={setActivePanel}
        apiOnline={apiOnline}
      />

      <main className="main-panel">
        {activePanel === "dashboard" && (
          <DashboardPanel
            apiOnline={apiOnline}
            facts={facts}
            capabilities={capabilities}
            runCommand={runCommand}
            notify={notify}
          />
        )}

        {activePanel === "chat" && (
          <ChatPanel
            messages={messages}
            loading={loading}
            input={input}
            setInput={setInput}
            sendMessage={sendMessage}
            handleKeyDown={handleKeyDown}
          />
        )}

        {activePanel === "voice" && <VoicePanel runCommand={runCommand} />}


        {activePanel === "projects" && <ProjectPanel runCommand={runCommand} />}

        {activePanel === "memory" && (
          <MemoryPanel runCommand={runCommand} loadFacts={loadFacts} />
        )}

        {activePanel === "tools" && <ToolsPanel runCommand={runCommand} />}


        {activePanel === "logs" && <LogsPanel runCommand={runCommand} />}

        {activePanel === "settings" && (
          <SettingsPanel
            modelSettings={modelSettings}
            setModelSettings={setModelSettings}
            ollamaModels={ollamaModels}
            modelTestResult={modelTestResult}
            performanceData={performanceData}
            promptTemplates={promptTemplates}
            setPromptTemplates={setPromptTemplates}
            routeInput={routeInput}
            setRouteInput={setRouteInput}
            routePreview={routePreview}
            loadOllamaModels={loadOllamaModels}
            saveModelSettings={saveModelSettings}
            testSelectedModel={testSelectedModel}
            testPerformance={testPerformance}
            previewRoute={previewRoute}
            savePromptTemplates={savePromptTemplates}
          />
        )}
      </main>
    </div>
  );
}

export default App;