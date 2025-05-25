const { app, BrowserWindow, Tray, Menu, clipboard } = require('electron');
const path = require('path');
const { exec } = require('child_process');

let tray = null;
let win = null;
let ngrokURL = 'Starting...';

function createWindow() {
  win = new BrowserWindow({
    width: 600,
    height: 400,
    webPreferences: {
      contextIsolation: false,
      nodeIntegration: true
    }
  });
  win.loadFile('public/index.html');
}

function startRelayServer() {
  exec('node relayui/server.js', (err, stdout, stderr) => {
    if (err) console.error('Relay server error:', err);
  });
}

function startNgrokTunnel() {
  const ngrokProcess = exec('ngrok http 3001');
  ngrokProcess.stdout.on('data', data => {
    const match = data.toString().match(/https?:\/\/[^\s]+/);
    if (match) {
      ngrokURL = match[0];
      updateTray();
    }
  });
}

function updateTray() {
  const contextMenu = Menu.buildFromTemplate([
    { label: 'Copy ngrok URL', click: () => clipboard.writeText(ngrokURL) },
    { label: 'Open UI', click: () => win.show() },
    { label: 'Quit', click: () => app.quit() }
  ]);
  tray.setToolTip(`Relay running\n${ngrokURL}`);
  tray.setContextMenu(contextMenu);
}

app.whenReady().then(() => {
  createWindow();
  tray = new Tray(path.join(__dirname, 'public', 'relay_icon.png'));
  startRelayServer();
  startNgrokTunnel();
});