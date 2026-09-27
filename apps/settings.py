import tkinter as tk


class SettingsApp:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#1e1e2e")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="⚙️ MiniOS Settings",
                 bg="#1e1e2e", fg="#00d4ff",
                 font=("Courier", 16, "bold")).pack(pady=20)

        info = [
            "System: MiniOS v1.0",
            "Kernel: Python Tkinter",
            "Platform: Kali Linux",
            "",
            "Hotkeys:",
            "  F11   → Toggle Fullscreen",
            "  Esc   → Exit Fullscreen",
            "",
            "Window Manager: Built-in",
            "Apps: Terminal, Notepad, File Manager",
        ]
        for line in info:
            tk.Label(self.frame, text=line, bg="#1e1e2e", fg="#ccc",
                     font=("Courier", 10), anchor="w").pack(
                fill="x", padx=30, pady=2)
