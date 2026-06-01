import { apiGet, apiPost } from "./apiClient";


export async function getVoiceStatus() {
  return await apiGet("/voice/status");
}


export async function startVoiceMode() {
  return await apiPost("/voice/start", {});
}
