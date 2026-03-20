# 📚 Mathnasium PAR Comment Tool — Chrome Extension

## What's in this folder
```
📁 mathnasium_extension/
├── manifest.json   ← extension config (don't touch)
├── popup.html      ← the popup UI
├── popup.js        ← popup logic
├── background.js   ← automation logic
├── content.js      ← runs on Radius pages
└── icon.png        ← extension icon (add your own 128x128 PNG)
```

---

## How to Install (One Time)

1. Open Chrome and go to: **chrome://extensions**
2. Turn on **Developer Mode** (toggle in top right)
3. Click **"Load unpacked"**
4. Select this folder
5. The A⁺ icon will appear in your Chrome toolbar!

---

## How to Use

1. Log into Radius manually as usual
2. Click the **A⁺ icon** in the Chrome toolbar
3. Type the **student name** and **PAR comment**
4. Click **Submit**
5. The extension opens Radius, finds the student, and submits automatically!

---

## Important Notes
- You must be **logged into Radius** before using the tool
- If your session expires, just log back in and use the tool again
- Keep all files in the same folder — don't move them separately
