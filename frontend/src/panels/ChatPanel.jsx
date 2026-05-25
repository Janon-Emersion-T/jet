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
      <h2>Chat Panel</h2>

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
          placeholder="Type a JARVIS command..."
        />

        <button onClick={() => sendMessage()} disabled={loading}>
          <Send size={18} />
        </button>
      </div>
    </section>
  );
}
