const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("jarvisDesktop", {
  isElectron: true,
  notify: (payload) => ipcRenderer.invoke("notify", payload),
  quitApp: () => ipcRenderer.invoke("quit-app"),
});
