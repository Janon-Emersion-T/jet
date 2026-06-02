import { apiGet, apiPost } from "./apiClient";

export async function getLearningOverview(limit = 12) {
  return await apiGet(`/learning/overview?limit=${limit}`);
}

export async function getLearningStatus() {
  return await apiGet("/learning/status");
}

export async function startLearning() {
  return await apiPost("/learning/start", {});
}

export async function stopLearning() {
  return await apiPost("/learning/stop", {});
}

export async function runLearningCycle() {
  return await apiPost("/learning/run-once", {});
}

export async function runLearningBurst(maxCycles = 4) {
  return await apiPost(`/learning/burst?max_cycles=${maxCycles}`, {});
}

export async function runManualLearning(taskId) {
  return await apiPost("/learning/manual-run", { task_id: taskId });
}
