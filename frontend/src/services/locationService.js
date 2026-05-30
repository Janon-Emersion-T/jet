import { API_URL } from "../config/api";

export function getBrowserLocation() {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error("Geolocation is not supported on this system."));
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        resolve({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          accuracy: position.coords.accuracy,
          source: "browser",
        });
      },
      (error) => {
        reject(new Error(error.message || "Location permission denied."));
      },
      {
        enableHighAccuracy: true,
        timeout: 15000,
        maximumAge: 300000,
      }
    );
  });
}

export async function saveLocationToJarvis(location) {
  const res = await fetch(`${API_URL}/location/save`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(location),
  });

  if (!res.ok) {
    throw new Error(`Location save failed with status ${res.status}`);
  }

  return await res.json();
}

export async function detectLocationByIp() {
  const res = await fetch(`${API_URL}/location/detect-ip`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    throw new Error(`IP location detection failed with status ${res.status}`);
  }

  return await res.json();
}

export async function captureLocationForJarvis() {
  try {
    const browserLocation = await getBrowserLocation();
    await saveLocationToJarvis(browserLocation);

    return {
      ok: true,
      source: "browser",
      message: "Precise browser location saved.",
    };
  } catch (browserError) {
    const ipLocation = await detectLocationByIp();

    if (!ipLocation.ok) {
      throw new Error(ipLocation.message || "Location detection failed.");
    }

    return {
      ok: true,
      source: "ip",
      message: "Approximate IP-based location saved.",
    };
  }
}

export function shouldCaptureLocation(message) {
  const text = String(message || "").toLowerCase().trim();

  const exactTriggers = [
    "location",
    "my location",
    "current location",
    "where am i",
    "where am i located",
    "weather",
    "weather here",
    "weather near me",
    "weather for my location",
    "today weather",
    "current weather",
    "check weather",
    "check the weather",
    "what is the weather",
    "what's the weather",
  ];

  if (exactTriggers.includes(text)) {
    return true;
  }

  return (
    text.includes("weather here") ||
    text.includes("weather near me") ||
    text.includes("my location") ||
    text.includes("current location")
  );
}