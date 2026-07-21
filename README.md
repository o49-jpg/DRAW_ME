# 🧭 Aether Browser

A feature-rich custom web browser built specifically for developer environments like **GitHub Codespaces**.

---

## 🚀 Newly Added Features

1. **Persistent Bookmarks & Bookmarks Bar**:
   - Save any page instantly using the star icon (`⭐`) in the URL bar.
   - Access all bookmarks instantly from the interactive Bookmarks Bar below the navigation toolbar. Bookmarks are persistently saved to `userData/bookmarks.json`.
2. **Browsing History Manager (`about:history`)**:
   - Every visited page is automatically recorded with timestamps.
   - Click the History icon (`🕒`) in the toolbar or type `about:history` to view, search, and clear your browsing history.
3. **Built-in Ad-Blocker & Tracker Shield**:
   - Automatically intercepts and blocks requests to known ad networks and tracking domains (Google Syndication, DoubleClick, AdNxs, Analytics, Hotjar, etc.) at the network session level.
4. **Real-time Download Manager & Toast Notifications**:
   - Automatically tracks file downloads via Electron's `will-download` session API and displays a clean floating progress toast notification in the bottom right corner.
5. **Custom Settings Page (`about:settings`)**:
   - Customize your default search engine (Google, DuckDuckGo, Brave Search) and manage privacy data.
6. **Chrome & Firefox Extension Support**:
   - Place any unpacked WebExtension into `my-custom-browser/extensions/`, and it will automatically load on startup.
7. **Developer Tools & Inspect Element**:
   - Right-click any element on any webpage and select **Inspect Element** to open Chrome DevTools targeted directly at that element.

---

## 🛠️ How to Run in GitHub Codespaces

1. **Install Dependencies**:
   ```bash
   cd my-custom-browser
   npm install
   ```

2. **Run with Virtual Framebuffer (Xvfb)**:
   ```bash
   sudo apt-get update && sudo apt-get install -y xvfb libnss3 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libasound2
   npx electron .
   ```
