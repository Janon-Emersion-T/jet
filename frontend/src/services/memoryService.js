import { apiGet } from "./apiClient";
import { apiPost } from "./apiClient";

export async function getFacts() {
  return await apiGet("/facts");
}

export async function searchMemory(query) {
  return await apiPost("/memory/search", { query });
}

export async function getRecentMemories(limit = 20) {
  return await apiGet(`/memory/recent?limit=${limit}`);
}

export async function getMemoryOverview(limit = 12) {
  return await apiGet(`/memory/overview?limit=${limit}`);
}
