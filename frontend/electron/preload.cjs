const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("jarvisDesktop", {
  isElectron: true,
  apiUrl: process.env.JARVIS_API_URL || "http://127.0.0.1:8000",
  notify: (payload) => ipcRenderer.invoke("notify", payload),
  quitApp: () => ipcRenderer.invoke("quit-app"),
});
