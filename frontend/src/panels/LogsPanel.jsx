import { Bell } from "lucide-react";
import Panel from "../components/Panel";

export default function LogsPanel({ runCommand }) {
  return (
    <Panel title="Logs Panel UI" icon={<Bell />}>
      <div className="quick-grid">
        <button onClick={() => runCommand("read error logs")}>Read Error Logs</button>
        <button onClick={() => runCommand("laravel logs")}>Analyze Laravel Logs</button>
        <button onClick={() => runCommand("coding session summary")}>
          Session Summary
        </button>
      </div>
    </Panel>
  );
}

