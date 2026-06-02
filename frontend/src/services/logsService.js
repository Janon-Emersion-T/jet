import { apiGet } from "./apiClient";

export async function getActivitySummary(limit = 120) {
  return await apiGet(`/activity/summary?limit=${limit}`);
}
