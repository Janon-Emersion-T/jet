import { Folder } from "lucide-react";
import Panel from "../components/Panel";

export default function ProjectPanel({ runCommand }) {
  return (
    <Panel title="Project Panel UI" icon={<Folder />}>
      <div className="quick-grid">
        <button onClick={() => runCommand("list projects")}>List Projects</button>
        <button onClick={() => runCommand("current project")}>Current Project</button>
        <button onClick={() => runCommand("auto project")}>Auto Detect Project</button>
        <button onClick={() => runCommand("analyze project jarvis")}>Analyze JARVIS</button>
      </div>
    </Panel>
  );
}
