import { Database } from "lucide-react";
import Panel from "../components/Panel";

export default function MemoryPanel({ runCommand, loadFacts }) {
  return (
    <Panel title="Memory Panel UI" icon={<Database />}>
      <div className="quick-grid">
        <button onClick={() => runCommand("what do you remember")}>
          Show Facts
        </button>

        <button onClick={() => runCommand("search memory jarvis")}>
          Search JARVIS Memory
        </button>

        <button onClick={loadFacts}>
          Refresh Facts
        </button>
      </div>
    </Panel>
  );
}
