import DashboardPanel from "../panels/DashboardPanel";
import ChatPanel from "../panels/ChatPanel";
import ProjectPanel from "../panels/ProjectPanel";
import LearningPanel from "../panels/LearningPanel";
import MemoryPanel from "../panels/MemoryPanel";
import ToolsPanel from "../panels/ToolsPanel";
import LogsPanel from "../panels/LogsPanel";
import SettingsPanel from "../panels/SettingsPanel";


export const panelRegistry = {
  dashboard: DashboardPanel,
  chat: ChatPanel,
  projects: ProjectPanel,
  learning: LearningPanel,
  memory: MemoryPanel,
  tools: ToolsPanel,
  logs: LogsPanel,
  settings: SettingsPanel,
};
