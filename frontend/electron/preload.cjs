const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("jarvisDesktop", {
  notify: (payload) => ipcRenderer.invoke("notify", payload),
  quitApp: () => ipcRenderer.invoke("quit-app"),
});