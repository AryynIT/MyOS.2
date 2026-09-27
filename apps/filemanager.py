import tkinter as tk
import os
from tkinter import messagebox


class FileManagerApp:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#1e1e2e")
        self.frame.pack(fill="both", expand=True)

        self.cwd = os.path.expanduser("~")

        topbar = tk.Frame(self.frame, bg="#2a2a3e")
        topbar.pack(fill="x")

        tk.Button(topbar, text="⬆ Up", bg="#2a2a3e", fg="#fff",
                  relief="flat", font=("Courier", 9), padx=8, pady=4,
                  cursor="hand2", command=self.go_up).pack(side="left", padx=3)

        tk.Button(topbar, text="🏠 Home", bg="#2a2a3e", fg="#fff",
                  relief="flat", font=("Courier", 9), padx=8, pady=4,
                  cursor="hand2",
                  command=lambda: self.load_dir(os.path.expanduser("~"))
                  ).pack(side="left", padx=3)

        self.path_label = tk.Label(topbar, text="", bg="#2a2a3e", fg="#00d4ff",
                                    font=("Courier", 9))
        self.path_label.pack(side="left", padx=10)

        self.listbox = tk.Listbox(self.frame, bg="#1e1e2e", fg="#ddd",
                                   font=("Courier", 10),
                                   selectbackground="#00d4ff",
                                   selectforeground="#000",
                                   relief="flat", activestyle="none")
        self.listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.listbox.bind("<Double-Button-1>", self.open_item)

        self.load_dir(self.cwd)

    def load_dir(self, path):
        try:
            self.cwd = os.path.abspath(path)
            self.listbox.delete(0, "end")

            items = sorted(os.listdir(self.cwd))
            self.listbox.insert("end", "..  (parent)")
            for item in items:
                full = os.path.join(self.cwd, item)
                prefix = "📁 " if os.path.isdir(full) else "📄 "
                self.listbox.insert("end", prefix + item)

            self.path_label.config(text=self.cwd)
        except PermissionError:
            messagebox.showerror("Error", "Permission denied")

    def go_up(self):
        self.load_dir(os.path.dirname(self.cwd))

    def open_item(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        if idx == 0:
            self.go_up()
            return
        name = self.listbox.get(idx)[2:]  # strip emoji prefix
        full = os.path.join(self.cwd, name)
        if os.path.isdir(full):
            self.load_dir(full)
        else:
            try:
                with open(full, "r", errors="ignore") as f:
                    content = f.read(1000)
                messagebox.showinfo(name, content or "(empty)")
            except Exception as e:
                messagebox.showerror("Error", str(e))
