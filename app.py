import tkinter as tk
from tkinter import messagebox, ttk
import threading
import json
import os
import sys
from playwright.sync_api import sync_playwright

# ── Load config ────────────────────────────────────────────────────────────────
def get_config_path():
    """Works both in dev and when packaged with PyInstaller."""
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "config.json")

def get_session_path():
    """Session file lives next to the executable or script."""
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "session.json")

def load_credentials():
    path = get_config_path()
    if not os.path.exists(path):
        messagebox.showerror("Missing Config", f"config.json not found at:\n{path}")
        sys.exit(1)
    with open(path, "r") as f:
        data = json.load(f)
    return data["username"], data["password"]

# ── Playwright automation ──────────────────────────────────────────────────────
def run_automation(student_name, comment, status_callback):
    username, password = load_credentials()
    session_path = get_session_path()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # Load saved session if it exists
        if os.path.exists(session_path):
            context = browser.new_context(storage_state=session_path)
        else:
            context = browser.new_context()

        page = context.new_page()

        try:
            # Step 1: Check if already logged in
            page.goto("https://radius.mathnasium.com")
            page.wait_for_load_state("networkidle")

            if "Login" in page.url:
                status_callback("Logging in...")
                page.goto("https://radius.mathnasium.com/Account/Login")
                page.fill('input[name="UserName"]', username)
                page.fill('input[name="Password"]', password)
                page.click('input[type="submit"]')
                page.wait_for_load_state("networkidle")

                # Save session for next time
                context.storage_state(path=session_path)
                status_callback("Session saved!")
            else:
                status_callback("Already logged in!")

            # Step 2: Search for student
            status_callback("Searching for student...")
            page.click('a#SearchIcon')
            page.wait_for_load_state("networkidle")

            page.fill('input[name="ContactSearch"]', student_name)
            page.press('input[name="ContactSearch"]', "Enter")

            # Step 3: Navigate to student page
            status_callback("Opening student profile...")
            #page.wait_for_selector('a.linker[href*="/Student/Details/"]')
            #page.wait_for_load_state("networkidle")
            student_link = page.locator('a.linker[href*="/Student/Details/"]').first.get_attribute('href')
            page.goto(f"https://radius.mathnasium.com{student_link}")
            page.wait_for_load_state("networkidle")

            # Step 4: Navigate to account
            status_callback("Opening account...")
            account_link = page.locator('dt:has-text("Account") + dd a').get_attribute('href')
            page.goto(f"https://radius.mathnasium.com{account_link}")
            page.wait_for_load_state("networkidle")

            # Step 5: Log activity
            status_callback("Logging activity...")
            page.click('#LogActivity')
            page.fill('input[name="ActivitySubject"]', "PAR")
            page.fill('#ActivityComments', comment)
            page.click('input[onclick="ActivityClose()"]')
            #page.click('input[onclick="SaveActivity()"]')

            status_callback("✅ Done!")
            messagebox.showinfo("Success", f"Comment submitted for {student_name}!")

        except Exception as e:
            status_callback("❌ Error occurred.")
            messagebox.showerror("Error", str(e))

        finally:
            browser.close()

# ── Tkinter UI ─────────────────────────────────────────────────────────────────
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Mathnasium PAR Comment Tool")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")

        # Title
        tk.Label(
            root, text="📚 Mathnasium PAR Comment Tool",
            font=("Helvetica", 14, "bold"),
            bg="#1a1a2e", fg="#e94560"
        ).pack(pady=(20, 10))

        # Student Name
        tk.Label(root, text="Student Name", font=("Helvetica", 10),
                 bg="#1a1a2e", fg="#ffffff").pack(anchor="w", padx=40)
        self.name_entry = tk.Entry(root, font=("Helvetica", 11), width=35,
                                   bg="#16213e", fg="white",
                                   insertbackground="white", relief="flat")
        self.name_entry.pack(padx=40, pady=(2, 10), ipady=5)

        # Comment
        tk.Label(root, text="Comment", font=("Helvetica", 10),
                 bg="#1a1a2e", fg="#ffffff").pack(anchor="w", padx=40)
        self.comment_entry = tk.Text(root, font=("Helvetica", 11), width=35,
                                     height=4, bg="#16213e", fg="white",
                                     insertbackground="white", relief="flat")
        self.comment_entry.pack(padx=40, pady=(2, 10))

        # Submit Button
        self.submit_btn = tk.Button(
            root, text="Submit", font=("Helvetica", 11, "bold"),
            bg="#e94560", fg="white", relief="flat",
            padx=20, pady=6, cursor="hand2",
            command=self.on_submit
        )
        self.submit_btn.pack(pady=5)

        # Status label
        self.status_var = tk.StringVar(value="")
        tk.Label(root, textvariable=self.status_var,
                 font=("Helvetica", 9, "italic"),
                 bg="#1a1a2e", fg="#aaaaaa").pack(pady=(5, 0))

    def on_submit(self):
        name = self.name_entry.get().strip()
        comment = self.comment_entry.get("1.0", tk.END).strip()

        if not name or not comment:
            messagebox.showwarning("Missing Fields", "Please fill in both fields.")
            return

        # Disable button while running
        self.submit_btn.config(state="disabled", text="Running...")
        self.status_var.set("Starting...")

        # Run in a separate thread so UI doesn't freeze
        thread = threading.Thread(
            target=self._run_thread,
            args=(name, comment),
            daemon=True
        )
        thread.start()

    def _run_thread(self, name, comment):
        def update_status(msg):
            self.status_var.set(msg)

        run_automation(name, comment, update_status)

        # Re-enable button after done
        self.submit_btn.config(state="normal", text="Submit")

        # Clear fields after successful submission
        self.name_entry.delete(0, tk.END)
        self.comment_entry.delete("1.0", tk.END)


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()