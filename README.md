# A⁺ Mathnasium PAR Comment Tool

A desktop automation tool that submits PAR comments to the Mathnasium Radius portal — built with Python, Tkinter, and Playwright.

Instead of manually navigating the Radius website each time, staff can simply enter a student name and comment, click Submit, and the tool handles the rest automatically.

---

## How It Works

1. User enters a student name and PAR comment in the app
2. Playwright opens a browser and logs into Radius
3. Searches for the student → navigates to their account
4. Fills in the PAR comment and submits
5. Browser closes and fields are cleared for the next entry

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Tkinter | Desktop UI |
| Playwright | Browser automation |
| PyInstaller | Packaging into .exe |

---

## Project Structure

```
📁 mathnasium_tool/
├── app.py          ← main app (UI + automation)
├── config.json     ← login credentials (never commit this!)
├── session.json    ← saved session after first login (auto-created)
├── run.bat         ← double-click to run (Windows)
└── README.md
```

---

## Setup (Developer)

### 1. Clone the repo
```bash
git clone https://github.com/your-username/mathnasium-par-tool
cd mathnasium-par-tool
```

### 2. Install dependencies
```bash
pip install playwright pyinstaller
playwright install chromium
```

### 3. Add credentials
Create a `config.json` file in the project root:
```json
{
  "username": "your_radius_username",
  "password": "your_radius_password"
}
```

### 4. Run the app
```bash
python app.py
```

---

## Running for Non-Developers (Windows)

For users who don't have Python installed, just double-click **`run.bat`**. It will:
- Check if Python is installed (opens download page if not)
- Automatically install Playwright if missing
- Automatically install Chromium if missing
- Launch the app once everything is ready

> ⚠️ During Python installation, make sure to check **"Add python.exe to PATH"**

---

## Package as Standalone .exe

To distribute to users without requiring any installation:

**Windows:**
```bash
python -m PyInstaller --onefile --windowed --add-data "config.json;." app.py
```

**Mac:**
```bash
python -m PyInstaller --onefile --windowed --add-data "config.json:." app.py
```

Output will be in the `dist/` folder. Send users the `app.exe` + `config.json` together.

---

## Session Handling

- On first run the app logs in and saves the session to `session.json`
- Subsequent runs reuse the saved session — no login needed
- If the session expires, the app logs in automatically and saves a new session

---

## ⚠️ Security Notes

- **Never commit `config.json`** — it contains login credentials
- **Never commit `session.json`** — it contains active session tokens
- Both are excluded via `.gitignore`
