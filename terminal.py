import tkinter as tk
import subprocess
import os


class TerminalApp:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#000")
        self.frame.pack(fill="both", expand=True)

        self.output = tk.Text(self.frame, bg="#000", fg="#0f0",
                              font=("Courier", 10), insertbackground="#0f0",
                              relief="flat", wrap="word")
        self.output.pack(fill="both", expand=True, padx=5, pady=5)

        self.input_frame = tk.Frame(self.frame, bg="#000")
        self.input_frame.pack(fill="x", padx=5, pady=(0, 5))

        tk.Label(self.input_frame, text="$", bg="#000", fg="#0f0",
                 font=("Courier", 10, "bold")).pack(side="left")

        self.entry = tk.Entry(self.input_frame, bg="#000", fg="#0f0",
                              font=("Courier", 10), insertbackground="#0f0",
                              relief="flat")
        self.entry.pack(side="left", fill="x", expand=True, padx=5)
        self.entry.bind("<Return>", self.run_command)
        self.entry.focus_set()

        self.cwd = os.path.expanduser("~")
        self.output.insert("end", f"MiniOS Terminal v1.0\ncwd: {self.cwd}\n\n")

    def run_command(self, event=None):
        cmd = self.entry.get().strip()
        self.entry.delete(0, "end")
        if not cmd:
            return

        self.output.insert("end", f"$ {cmd}\n")

        if cmd.startswith("cd "):
            path = cmd[3:].strip()
            target = os.path.join(self.cwd, path) if not path.startswith("/") else path
            target = os.path.abspath(target)
            if os.path.isdir(target):
                self.cwd = target
                self.output.insert("end", f"→ {self.cwd}\n\n")
            else:
                self.output.insert("end", f"cd: no such directory: {path}\n\n")
            self.output.see("end")
            return

        if cmd == "clear":
            self.output.delete("1.0", "end")
            return

        try:
            result = subprocess.run(
                cmd, shell=True, cwd=self.cwd,
                capture_output=True, text=True, timeout=10
            )
            if result.stdout:
                self.output.insert("end", result.stdout)
            if result.stderr:
                self.output.insert("end", result.stderr)
        except Exception as e:
            self.output.insert("end", f"error: {e}\n")

        self.output.insert("end", "\n")
        self.output.see("end")
