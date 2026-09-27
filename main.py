#!/usr/bin/env python3
"""
MiniOS - Desktop Environment berbasis Tkinter
Jalan di terminal Kali Linux. Support Window Mode & Fullscreen Mode.
"""
import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from window_manager import WindowManager


class MiniOS:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MiniOS")
        self.root.geometry("1024x700")
        self.root.configure(bg="#0a0a0f")

        # Fullscreen mode via F11
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

        # Boot screen dulu
        self.show_boot()

    def show_boot(self):
        boot = tk.Frame(self.root, bg="#0a0a0f")
        boot.pack(fill="both", expand=True)

        tk.Label(boot, text="⚡ MiniOS", fg="#00d4ff", bg="#0a0a0f",
                 font=("Courier", 32, "bold")).pack(pady=(200, 20))

        self.status = tk.Label(boot, text="Booting kernel...",
                               fg="#888", bg="#0a0a0f",
                               font=("Courier", 12))
        self.status.pack()

        self.progress = tk.Canvas(boot, width=400, height=10,
                                  bg="#1a1a2e", highlightthickness=0)
        self.progress.pack(pady=20)
        self.bar = self.progress.create_rectangle(0, 0, 0, 10,
                                                  fill="#00d4ff", width=0)

        self.animate_boot(0)

    def animate_boot(self, value):
        steps = [
            (20, "Loading drivers..."),
            (40, "Mounting filesystem..."),
            (60, "Starting window manager..."),
            (80, "Loading applications..."),
            (100, "Ready."),
        ]
        if value >= len(steps):
            self.root.after(400, self.start_desktop)
            return
        pct, text = steps[value]
        self.progress.coords(self.bar, 0, 0, 400 * (pct / 100), 10)
        self.status.config(text=text)
        self.root.after(400, lambda: self.animate_boot(value + 1))

    def start_desktop(self):
        for w in self.root.winfo_children():
            w.destroy()

        self.wm = WindowManager(self.root, self.toggle_fullscreen)

    def toggle_fullscreen(self, event=None):
        current = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not current)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    MiniOS().run()
