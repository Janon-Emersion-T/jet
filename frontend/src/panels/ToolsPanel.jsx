import { ListChecks } from "lucide-react";
import Panel from "../components/Panel";

export default function ToolsPanel({ runCommand }) {
  return (
    <Panel title="Tools Panel UI" icon={<ListChecks />}>
      <div className="quick-grid">
        <button onClick={() => runCommand("git status")}>Git Status</button>
        <button onClick={() => runCommand("git diff")}>Git Diff</button>
        <button onClick={() => runCommand("inspect dependencies")}>
          Inspect Dependencies
        </button>
        <button onClick={() => runCommand("project health score")}>
          Health Score
        </button>
      </div>
    </Panel>
  );
}
