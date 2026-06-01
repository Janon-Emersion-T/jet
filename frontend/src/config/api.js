const desktopApiUrl =
  typeof window !== "undefined" && window.jarvisDesktop?.apiUrl
    ? window.jarvisDesktop.apiUrl
    : null;

export const API_URL =
  desktopApiUrl ||
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";
