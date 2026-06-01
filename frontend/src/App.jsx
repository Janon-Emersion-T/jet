import { useCallback, useEffect, useState } from "react";

import {
  captureLocationForJarvis,
  shouldCaptureLocation,
} from "./services/locationService";

import { getStartupGreeting } from "./utils/greeting";

import ChatHistoryPanel from "./components/ChatHistoryPanel";

import { useSystemPolling } from "./hooks/useSystemPolling";

import SocialChannelPanel from "./panels/SocialChannelPanel";

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

import {
  sendChatMessage,
  getChatSessions,
  createChatSession,
  getChatSession,
  deleteChatSession,
} from "./services/chatService";

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
  const [messages, setMessages] = useState(() => [
    {
      role: "jarvis",
      text: getStartupGreeting("Janon"),
    },
  ]);
  const [modelSettings, setModelSettings] = useState({});
  const [ollamaModels, setOllamaModels] = useState([]);
  const [modelTestResult, setModelTestResult] = useState("");
  const [performanceData, setPerformanceData] = useState({});
  const [promptTemplates, setPromptTemplates] = useState({});
  const [routePreview, setRoutePreview] = useState(null);
  const [routeInput, setRouteInput] = useState("");
  const [chatSessions, setChatSessions] = useState([]);
  const [activeChatId, setActiveChatId] = useState(null);

  const checkApi = useCallback(async () => {
    try {
      const data = await checkApiStatus();
      setApiOnline(data.status === "online");
    } catch {
      setApiOnline(false);
    }
  }, []);

  const loadFacts = useCallback(async () => {
    try {
      const data = await getFacts();
      setFacts(data.facts || []);
    } catch {
      setFacts([]);
    }
  }, []);

  const loadCapabilities = useCallback(async () => {
    try {
      const data = await getCapabilities();
      setCapabilities(data.capabilities || []);
    } catch {
      setCapabilities([]);
    }
  }, []);

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

  async function loadChatSessions() {
    try {
      const data = await getChatSessions();
      setChatSessions(data.sessions || []);

      if (!activeChatId && data.sessions?.length > 0) {
        await selectChat(data.sessions[0].id);
      }

      if (!activeChatId && (!data.sessions || data.sessions.length === 0)) {
        await createNewChat();
      }
    } catch {
      setChatSessions([]);
    }
  }

  async function createNewChat() {
    const data = await createChatSession();
    const session = data.session;

    setActivePanel("chat");
    setActiveChatId(session.id);
    setMessages(session.messages || []);
    await refreshChatListOnly();
  }

  async function refreshChatListOnly() {
    try {
      const data = await getChatSessions();
      setChatSessions(data.sessions || []);
    } catch {
      setChatSessions([]);
    }
  }

  async function selectChat(chatId) {
    const data = await getChatSession(chatId);
    const session = data.session;

    setActivePanel("chat");
    setActiveChatId(session.id);
    setMessages(session.messages || []);
    await refreshChatListOnly();
  }

  async function deleteChat(chatId) {
    await deleteChatSession(chatId);

    const data = await getChatSessions();
    const sessions = data.sessions || [];

    setChatSessions(sessions);

    if (activeChatId === chatId) {
      if (sessions.length > 0) {
        await selectChat(sessions[0].id);
      } else {
        await createNewChat();
      }
    }
  }


  useEffect(() => {
    loadModelSettings();
    loadOllamaModels();
    loadPerformanceData();
    loadPromptTemplates();
    loadChatSessions();
  }, []);

  useSystemPolling({
    checkApi,
    loadFacts,
    loadCapabilities,
    intervalMs: 30000,
  });

  async function notify(title, body) {
    if (window.jarvisDesktop?.notify) {
      await window.jarvisDesktop.notify({ title, body });
    }
  }

  async function sendMessage(customMessage = null) {
    const message = (customMessage || input).trim();

    if (!message || loading) return;

    if (message.length < 2) {
      return;
    }

    setMessages((prev) => [...prev, { role: "user", text: message }]);
    setInput("");
    setLoading(true);

    try {
      if (shouldCaptureLocation(message)) {
        try {
          await captureLocationForJarvis();
        } catch (locationError) {
          setMessages((prev) => [
            ...prev,
            {
              role: "jarvis",
              text:
                "Location detection failed. " +
                "Browser location and IP-based fallback both failed. " +
                "You can still ask weather by city, for example: weather in Jaffna.",
            },
          ]);
          setLoading(false);
          return;
        }
      }

      let chatId = activeChatId;

      if (!chatId) {
        const newChat = await createChatSession();
        chatId = newChat.session.id;
        setActiveChatId(chatId);
      }

      const data = await sendChatMessage(message, chatId);

      if (data.session?.messages) {
        setMessages(data.session.messages);
      } else {
        setMessages((prev) => [
          ...prev,
          {
            role: "jarvis",
            text: data.response || "No response received.",
          },
        ]);
      }

      await refreshChatListOnly();
      const response = data.response || "No response received.";

      

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
    const safeCommand = String(command || "").trim();

    if (!safeCommand) return;

    setActivePanel("chat");
    sendMessage(safeCommand);
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="app-shell">
      <ChatHistoryPanel
        chatSessions={chatSessions}
        activeChatId={activeChatId}
        createNewChat={createNewChat}
        selectChat={selectChat}
        deleteChat={deleteChat}
        messages={messages}
        apiOnline={apiOnline}
      />

      <main className="main-panel jarvis-main">
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
        {["whatsapp", "facebook", "instagram", "linkedin", "tiktok", "email"].includes(
          activePanel
        ) && <SocialChannelPanel channel={activePanel} />}
      </main>
      <Sidebar
        activePanel={activePanel}
        setActivePanel={setActivePanel}
        apiOnline={apiOnline}
      />
    </div>
  );
}

export default App;