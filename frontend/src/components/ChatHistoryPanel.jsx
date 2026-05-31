import { MessageSquare, Plus, Trash2 } from "lucide-react";

export default function ChatHistoryPanel({
  chatSessions,
  activeChatId,
  createNewChat,
  selectChat,
  deleteChat,
  messages,
  apiOnline,
}) {
  return (
    <aside className="chat-history-panel">
      <div className="history-brand">
        <img src="/icon.png" className="brand-icon" alt="JARVIS" />

        <div>
          <h1>JARVIS</h1>
          <p>Conversation Context</p>
        </div>
      </div>

      <button className="new-chat-button" onClick={createNewChat}>
        <Plus size={18} />
        New chat
      </button>

      <div className="chat-history-list">
        {chatSessions.length === 0 && (
          <div className="empty-history">No chats yet.</div>
        )}

        {chatSessions.map((session) => (
          <button
            key={session.id}
            className={
              activeChatId === session.id
                ? "chat-history-item active"
                : "chat-history-item"
            }
            onClick={() => selectChat(session.id)}
          >
            <MessageSquare size={16} />

            <span>
              <strong>{session.title || "New chat"}</strong>
              <small>{session.message_count || 0} messages</small>
            </span>

            <Trash2
              size={15}
              className="chat-delete-icon"
              onClick={(event) => {
                event.stopPropagation();
                deleteChat(session.id);
              }}
            />
          </button>
        ))}
      </div>

      <div className="history-context">
        <h3>Current context</h3>

        <div className="history-context-feed">
          {messages.slice(-4).map((message, index) => (
            <div key={index} className={`context-message ${message.role}`}>
              {message.text.slice(0, 180)}
              {message.text.length > 180 ? "..." : ""}
            </div>
          ))}
        </div>
      </div>

      <div className="history-footer">
        <span className={apiOnline ? "dot online" : "dot offline"} />
        {apiOnline ? "API Online" : "API Offline"}
      </div>
    </aside>
  );
}
