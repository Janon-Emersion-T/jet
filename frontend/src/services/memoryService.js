import { apiGet } from "./apiClient";

export async function getFacts() {
  return await apiGet("/facts");
}