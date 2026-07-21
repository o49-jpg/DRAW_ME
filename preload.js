const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  minimizeWindow: () => ipcRenderer.send('window-minimize'),
  maximizeWindow: () => ipcRenderer.send('window-maximize'),
  closeWindow: () => ipcRenderer.send('window-close'),

  // Bookmarks
  getBookmarks: () => ipcRenderer.invoke('get-bookmarks'),
  saveBookmarks: (bookmarks) => ipcRenderer.invoke('save-bookmarks', bookmarks),

  // History
  getHistory: () => ipcRenderer.invoke('get-history'),
  addHistory: (item) => ipcRenderer.invoke('add-history', item),
  clearHistory: () => ipcRenderer.invoke('clear-history'),

  // Download listeners
  onDownloadStarted: (callback) => ipcRenderer.on('download-started', (e, data) => callback(data)),
  onDownloadProgress: (callback) => ipcRenderer.on('download-progress', (e, data) => callback(data)),
  onDownloadComplete: (callback) => ipcRenderer.on('download-complete', (e, data) => callback(data)),
  onDownloadFailed: (callback) => ipcRenderer.on('download-failed', (e, data) => callback(data))
});
