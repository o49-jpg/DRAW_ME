const { app, BrowserWindow, session, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs');

let mainWindow;

// Paths for persistent data (bookmarks & history)
const userDataPath = app.getPath('userData');
const bookmarksFile = path.join(userDataPath, 'bookmarks.json');
const historyFile = path.join(userDataPath, 'history.json');

function loadJSON(filePath, defaultData) {
  try {
    if (fs.existsSync(filePath)) {
      return JSON.parse(fs.readFileSync(filePath, 'utf8'));
    }
  } catch (err) {
    console.error(`Error loading ${filePath}:`, err);
  }
  return defaultData;
}

function saveJSON(filePath, data) {
  try {
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
  } catch (err) {
    console.error(`Error saving ${filePath}:`, err);
  }
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    frame: false,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      webviewTag: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  mainWindow.loadFile(path.join(__dirname, 'src', 'index.html'));

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Load Chrome/Firefox (unpacked WebExtension) extensions on startup
async function loadExtensions() {
  const extensionsDir = path.join(__dirname, 'extensions');
  if (!fs.existsSync(extensionsDir)) {
    fs.mkdirSync(extensionsDir, { recursive: true });
  }

  try {
    const entries = fs.readdirSync(extensionsDir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.isDirectory()) {
        const extPath = path.join(extensionsDir, entry.name);
        await session.defaultSession.loadExtension(extPath);
        console.log(`Loaded extension: ${entry.name}`);
      }
    }
  } catch (err) {
    console.error('Error loading extensions:', err);
  }
}

// Feature 1: Built-in Ad-Blocker & Tracker Filter
function setupAdBlocker() {
  const blockedDomains = [
    'googlesyndication.com',
    'adservice.google.com',
    'doubleclick.net',
    'adnxs.com',
    'amazon-adsystem.com',
    'facebook.com/tr',
    'google-analytics.com',
    'hotjar.com'
  ];

  session.defaultSession.webRequest.onBeforeRequest({ urls: ['<all_urls>'] }, (details, callback) => {
    const url = details.url;
    const isBlocked = blockedDomains.some(domain => url.includes(domain));
    if (isBlocked) {
      // Cancel request
      callback({ cancel: true });
    } else {
      callback({ cancel: false });
    }
  });
}

// Feature 2: Download Manager
function setupDownloadManager() {
  session.defaultSession.on('will-download', (event, item, webContents) => {
    const fileName = item.getFilename();
    const fileSize = item.getTotalBytes();
    console.log(`Downloading: ${fileName} (${fileSize} bytes)`);

    if (mainWindow) {
      mainWindow.webContents.send('download-started', { name: fileName, size: fileSize });
    }

    item.on('updated', (event, state) => {
      if (state === 'progressing') {
        const progress = item.getReceivedBytes() / fileSize;
        if (mainWindow) {
          mainWindow.webContents.send('download-progress', { name: fileName, progress });
        }
      }
    });

    item.once('done', (event, state) => {
      if (state === 'completed') {
        console.log(`Download completed: ${fileName}`);
        if (mainWindow) {
          mainWindow.webContents.send('download-complete', { name: fileName, path: item.getSavePath() });
        }
      } else {
        console.log(`Download failed: ${state}`);
        if (mainWindow) {
          mainWindow.webContents.send('download-failed', { name: fileName, state });
        }
      }
    });
  });
}

app.whenReady().then(async () => {
  setupAdBlocker();
  setupDownloadManager();
  await loadExtensions();
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC Handlers for Window Controls
ipcMain.on('window-minimize', () => {
  if (mainWindow) mainWindow.minimize();
});

ipcMain.on('window-maximize', () => {
  if (mainWindow) {
    if (mainWindow.isMaximized()) {
      mainWindow.unmaximize();
    } else {
      mainWindow.maximize();
    }
  }
});

ipcMain.on('window-close', () => {
  if (mainWindow) mainWindow.close();
});

// IPC Handlers for Bookmarks
ipcMain.handle('get-bookmarks', () => {
  return loadJSON(bookmarksFile, [
    { title: 'GitHub', url: 'https://github.com' },
    { title: 'Google', url: 'https://www.google.com' },
    { title: 'MDN Web Docs', url: 'https://developer.mozilla.org' }
  ]);
});

ipcMain.handle('save-bookmarks', (event, bookmarks) => {
  saveJSON(bookmarksFile, bookmarks);
  return true;
});

// IPC Handlers for History
ipcMain.handle('get-history', () => {
  return loadJSON(historyFile, []);
});

ipcMain.handle('add-history', (event, item) => {
  let history = loadJSON(historyFile, []);
  history.unshift({ ...item, timestamp: Date.now() });
  if (history.length > 500) history = history.slice(0, 500); // Keep last 500
  saveJSON(historyFile, history);
  return true;
});

ipcMain.handle('clear-history', () => {
  saveJSON(historyFile, []);
  return true;
});
