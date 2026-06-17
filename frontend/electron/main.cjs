const {
  app,
  BrowserWindow,
  Menu,
  Tray,
  Notification,
  ipcMain,
  session,
} = require("electron");

const path = require("path");
const fs = require("fs");

let mainWindow;
let tray;

app.commandLine.appendSwitch("no-sandbox");
app.commandLine.appendSwitch("disable-dev-shm-usage");

const DEV_URL = "http://localhost:5173";
const DIST_INDEX = path.join(__dirname, "../dist/index.html");

function resolveAppEntry() {
  const forceDev = process.env.JARVIS_ELECTRON_DEV === "1";
  if (!forceDev && fs.existsSync(DIST_INDEX)) {
    return { type: "file", value: DIST_INDEX };
  }
  return { type: "url", value: DEV_URL };
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1450,
    height: 900,
    minWidth: 1100,
    minHeight: 720,
    show: false,
    fullscreen: true,
    autoHideMenuBar: true,
    backgroundColor: "#050b14",
    title: "JARVIS - Local AI Workstation",
    webPreferences: {
      preload: path.join(__dirname, "preload.cjs"),
      nodeIntegration: false,
      contextIsolation: true,
      webviewTag: true,
    },
  });

  const entry = resolveAppEntry();
  if (entry.type === "file") {
    mainWindow.loadFile(entry.value);
  } else {
    mainWindow.loadURL(entry.value);
  }

  // mainWindow.maximize();

  mainWindow.once("ready-to-show", () => {
    mainWindow.show();
    mainWindow.focus();
  });

  mainWindow.on("close", (event) => {
    if (!app.isQuitting) {
      event.preventDefault();
      mainWindow.hide();
    }
  });
}

function createTray() {
  const iconPath = path.join(__dirname, "../public/favicon.svg");

  try {
    tray = new Tray(iconPath);
  } catch (error) {
    console.warn("Tray icon failed to load:", iconPath);
    return;
  }

  const menu = Menu.buildFromTemplate([
    {
      label: "Open JARVIS",
      click: () => {
        mainWindow.show();
        mainWindow.focus();
      },
    },
    {
      label: "Hide JARVIS",
      click: () => mainWindow.hide(),
    },
    { type: "separator" },
    {
      label: "Quit",
      click: () => {
        app.isQuitting = true;
        app.quit();
      },
    },
  ]);

  tray.setToolTip("JARVIS Local AI Workstation");
  tray.setContextMenu(menu);

  tray.on("double-click", () => {
    mainWindow.show();
    mainWindow.focus();
  });
}

ipcMain.handle("notify", async (_, payload) => {
  const title = payload?.title || "JARVIS";
  const body = payload?.body || "Notification";

  if (Notification.isSupported()) {
    new Notification({ title, body }).show();
    return { ok: true };
  }

  return { ok: false, error: "Notifications are not supported on this system." };
});

ipcMain.handle("quit-app", async () => {
  app.isQuitting = true;
  app.quit();
  return { ok: true };
});

app.whenReady().then(() => {
  session.defaultSession.setPermissionRequestHandler(
    (webContents, permission, callback) => {
      if (permission === "geolocation") {
        callback(true);
        return;
      }

      callback(false);
    }
  );

  createWindow();
  // createTray();

  new Notification({
    title: "JARVIS Online",
    body: "Desktop shell, tray, and dashboard are active.",
  }).show();
});

app.on("window-all-closed", (event) => {
  event.preventDefault();
});

app.on("activate", () => {
  if (!mainWindow) createWindow();
  mainWindow.show();
});
