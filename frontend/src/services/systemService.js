import { API_URL } from "../config/api";

export async function checkApiStatus() {
  const res = await fetch(`${API_URL}/`);
  return await res.json();
}

export async function getCapabilities() {
  const res = await fetch(`${API_URL}/capabilities`);
  return await res.json();
}
