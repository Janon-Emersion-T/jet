import {
  Activity,
  Brain,
  Database,
  Folder,
  Hammer,
  Mic,
  Settings,
  Terminal,
} from "lucide-react";

export const panels = [
  { id: "dashboard", label: "Dashboard", icon: Activity },
  { id: "chat", label: "Chat", icon: Brain },
  { id: "voice", label: "Voice", icon: Mic },
  { id: "projects", label: "Projects", icon: Folder },
  { id: "memory", label: "Memory", icon: Database },
  { id: "tools", label: "Tools", icon: Hammer },
  { id: "logs", label: "Logs", icon: Terminal },
  { id: "settings", label: "Settings", icon: Settings },
];
