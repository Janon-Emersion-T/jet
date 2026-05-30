import { apiGet } from "./apiClient";

export async function checkApiStatus() {
  return await apiGet("/");
}

export async function getCapabilities() {
  return await apiGet("/capabilities");
}