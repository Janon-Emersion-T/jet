import { apiGet, apiPost } from "./apiClient";

export async function getLearningOverview(limit = 12) {
  return await apiGet(`/learning/overview?limit=${limit}`);
}

export async function getLearningStatus() {
  return await apiGet("/learning/status");
}

export async function getLearningCatalog(params = {}) {
  const searchParams = new URLSearchParams();

  if (params.domain) searchParams.set("domain", params.domain);
  if (params.query) searchParams.set("query", params.query);
  if (params.limit) searchParams.set("limit", String(params.limit));

  const suffix = searchParams.toString() ? `?${searchParams.toString()}` : "";
  return await apiGet(`/learning/catalog${suffix}`);
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

export async function runManualLearning(payload) {
  return await apiPost("/learning/manual-run", payload);
}
