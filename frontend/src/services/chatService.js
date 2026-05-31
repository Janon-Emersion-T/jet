import { apiGet, apiPost } from "./apiClient";
import { API_URL } from "../config/api";

export async function sendChatMessage(message, chatId = null) {
  return await apiPost("/chat", {
    message,
    chat_id: chatId,
  });
}

export async function getChatSessions() {
  return await apiGet("/chats");
}

export async function createChatSession() {
  return await apiPost("/chats", {});
}

export async function getChatSession(chatId) {
  return await apiGet(`/chats/${chatId}`);
}

export async function renameChatSession(chatId, title) {
  return await apiPost(`/chats/${chatId}/rename`, { title });
}

export async function deleteChatSession(chatId) {
  const res = await fetch(`${API_URL}/chats/${chatId}`, {
    method: "DELETE",
  });

  if (!res.ok) {
    throw new Error(`DELETE /chats/${chatId} failed with status ${res.status}`);
  }

  return await res.json();
}