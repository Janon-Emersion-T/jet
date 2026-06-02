import { Send } from "lucide-react";

export default function ChatPanel({
  messages,
  loading,
  input,
  setInput,
  sendMessage,
  handleKeyDown,
}) {
  return (
    <section className="panel chat-panel">
      <div className="chat-header">
        <div>
          <p className="eyebrow">CONVERSATION</p>
          <h2>Talk to JARVIS naturally</h2>
        </div>
        <p className="chat-header-note">
          Ask normally by text or voice. JARVIS will decide the best next action.
        </p>
      </div>

      <div className="messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <pre>{message.text}</pre>
          </div>
        ))}

        {loading && <div className="message jarvis">Thinking...</div>}
      </div>

      <div className="composer">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask anything, describe a task, or tell JARVIS what to do..."
        />

        <button onClick={() => sendMessage()} disabled={loading}>
          <Send size={18} />
        </button>
      </div>
    </section>
  );
}
