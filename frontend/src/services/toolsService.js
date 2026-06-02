import { apiGet } from "./apiClient";

export async function getToolRegistry() {
  return await apiGet("/tools/registry");
}
