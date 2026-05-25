import { API_URL } from "../config/api";

export async function getFacts() {
  const res = await fetch(`${API_URL}/facts`);
  return await res.json();
}
