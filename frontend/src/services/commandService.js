import { apiGet, apiPost } from "./apiClient";


export async function runPanelCommand(command, source = "panel") {
  return await apiPost("/command", {
    command,
    source,
    save_to_memory: true,
  });
}


export async function getActivity(limit = 50) {
  return await apiGet(`/activity?limit=${limit}`);
}
