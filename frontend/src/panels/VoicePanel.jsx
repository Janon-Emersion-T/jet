import { Mic } from "lucide-react";
import Panel from "../components/Panel";

export default function VoicePanel({ runCommand }) {
  return (
    <Panel title="Voice Status UI" icon={<Mic />}>
      <p>Voice is still backend-terminal driven. UI can trigger the route safely.</p>

      <button onClick={() => runCommand("activate voice mode")}>
        Activate Voice Mode
      </button>
    </Panel>
  );
}
