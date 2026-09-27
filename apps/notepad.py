import tkinter as tk
from tkinter import filedialog, messagebox


class NotepadApp:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#1e1e2e")
        self.frame.pack(fill="both", expand=True)

        toolbar = tk.Frame(self.frame, bg="#2a2a3e")
        toolbar.pack(fill="x")

        for label, cmd in [("📂 Open", self.open_file),
                           ("💾 Save", self.save_file),
                           ("🗑 Clear", self.clear)]:
            tk.Button(toolbar, text=label, bg="#2a2a3e", fg="#fff",
                      relief="flat", font=("Courier", 9),
                      padx=10, pady=5, cursor="hand2",
                      command=cmd).pack(side="left", padx=2)

        self.text = tk.Text(self.frame, bg="#1e1e2e", fg="#e0e0e0",
                            font=("Courier", 11), insertbackground="#fff",
                            relief="flat", wrap="word", undo=True)
        self.text.pack(fill="both", expand=True, padx=5, pady=5)

        self.current_file = None

    def open_file(self):
        path = filedialog.askopenfilename()
        if not path:
            return
        try:
            with open(path, "r") as f:
                self.text.delete("1.0", "end")
                self.text.insert("1.0", f.read())
            self.current_file = path
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_file(self):
        if self.current_file:
            path = self.current_file
        else:
            path = filedialog.asksaveasfilename()
            if not path:
                return
        try:
            with open(path, "w") as f:
                f.write(self.text.get("1.0", "end-1c"))
            self.current_file = path
            messagebox.showinfo("Saved", f"Saved to {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear(self):
        self.text.delete("1.0", "end")
