import {
  Activity,
  Brain,
  BookOpen,
  Database,
  Folder,
  Hammer,
  Settings,
  Terminal,
} from "lucide-react";

export const panels = [
  { id: "dashboard", label: "Dashboard", icon: Activity },
  { id: "chat", label: "Chat", icon: Brain },
  { id: "projects", label: "Projects", icon: Folder },
  { id: "learning", label: "Learning", icon: BookOpen },
  { id: "memory", label: "Memory", icon: Database },
  { id: "tools", label: "Tools", icon: Hammer },
  { id: "logs", label: "Logs", icon: Terminal },
  { id: "settings", label: "Settings", icon: Settings },
];
