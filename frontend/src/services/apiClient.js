import { API_URL } from "../config/api";

export async function apiGet(path) {
  console.debug(`[JARVIS API] GET ${path}`);

  const res = await fetch(`${API_URL}${path}`);

  if (!res.ok) {
    throw new Error(`GET ${path} failed with status ${res.status}`);
  }

  return await res.json();
}

export async function apiPost(path, payload) {
  console.debug(`[JARVIS API] POST ${path}`, payload);

  const res = await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error(`POST ${path} failed with status ${res.status}`);
  }

  return await res.json();
}
