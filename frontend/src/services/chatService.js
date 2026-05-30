import { apiPost } from "./apiClient";

export async function sendChatMessage(message) {
  return await apiPost("/chat", { message });
}