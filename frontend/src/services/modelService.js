import { API_URL } from "../config/api";

export async function getModelSettings() {
  const res = await fetch(`${API_URL}/models/settings`);
  return await res.json();
}

export async function saveModelSettingsRequest(settings) {
  const res = await fetch(`${API_URL}/models/settings`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(settings),
  });

  return await res.json();
}

export async function getOllamaModels() {
  const res = await fetch(`${API_URL}/models/ollama`);
  return await res.json();
}

export async function testOllamaModel(model) {
  const res = await fetch(`${API_URL}/models/ollama/test`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ model }),
  });

  return await res.json();
}

export async function getModelPerformance() {
  const res = await fetch(`${API_URL}/models/performance`);
  return await res.json();
}

export async function testModelPerformance(model) {
  const res = await fetch(`${API_URL}/models/performance/test`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ model }),
  });

  return await res.json();
}

export async function getModelFallback(message) {
  const res = await fetch(`${API_URL}/models/fallback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  return await res.json();
}

export async function getPromptTemplates() {
  const res = await fetch(`${API_URL}/prompts/templates`);
  return await res.json();
}

export async function savePromptTemplatesRequest(templates) {
  const res = await fetch(`${API_URL}/prompts/templates`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(templates),
  });

  return await res.json();
}