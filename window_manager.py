import tkinter as tk
from datetime import datetime
from apps.terminal import TerminalApp
from apps.notepad import NotepadApp
from apps.filemanager import FileManagerApp
from apps.settings import SettingsApp


class WindowManager:
    def __init__(self, root, fullscreen_cb):
        self.root = root
        self.fullscreen_cb = fullscreen_cb
        self.z_index = 100
        self.windows = {}

        self.setup_desktop()
        self.setup_taskbar()
        self.setup_startmenu()
        self.start_clock()

    # ================= DESKTOP =================
    def setup_desktop(self):
        self.desktop = tk.Frame(self.root, bg="#16213e")
        self.desktop.pack(fill="both", expand=True)

        # Background gradient-ish pakai canvas
        self.canvas = tk.Canvas(self.desktop, bg="#16213e",
                                highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.close_startmenu)
        self.canvas.bind("<Configure>", self.redraw_bg)

        # Label hint
        self.canvas.create_text(
            20, 20, anchor="nw",
            text="MiniOS Desktop\nKlik 'Start' untuk buka aplikasi\nF11 = Fullscreen | Esc = Keluar Fullscreen",
            fill="#4a5578", font=("Courier", 10), tags="hint"
        )

    def redraw_bg(self, event=None):
        # Simulasi gradient
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10:
            return
        self.canvas.delete("bg")
        for i in range(30):
            ratio = i / 30
            r = int(0x1a + (0x0f - 0x1a) * ratio)
            g = int(0x1a + (0x34 - 0x1a) * ratio)
            b = int(0x2e + (0x60 - 0x2e) * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_rectangle(
                0, h * ratio, w, h * (ratio + 0.04),
                fill=color, width=0, tags="bg"
            )
        self.canvas.tag_raise("hint")

    # ================= TASKBAR =================
    def setup_taskbar(self):
        self.taskbar = tk.Frame(self.root, bg="#0f0f1a", height=40)
        self.taskbar.place(relx=0, rely=1, relwidth=1, anchor="sw")
        self.taskbar.pack_propagate(False)

        self.start_btn = tk.Button(
            self.taskbar, text="🪟 Start", bg="#1e1e2e", fg="#fff",
            activebackground="#2e2e4e", activeforeground="#fff",
            relief="flat", font=("Courier", 10, "bold"),
            padx=15, cursor="hand2",
            command=self.toggle_startmenu
        )
        self.start_btn.pack(side="left", padx=5, pady=5)

        self.task_list = tk.Frame(self.taskbar, bg="#0f0f1a")
        self.task_list.pack(side="left", fill="x", expand=True)

        self.clock = tk.Label(self.taskbar, text="", bg="#0f0f1a",
                              fg="#00d4ff", font=("Courier", 11, "bold"))
        self.clock.pack(side="right", padx=15)

    def start_clock(self):
        def tick():
            now = datetime.now().strftime("%H:%M:%S  %d/%m/%Y")
            self.clock.config(text=now)
            self.root.after(1000, tick)
        tick()

    # ================= START MENU =================
    def setup_startmenu(self):
        self.startmenu = tk.Frame(self.root, bg="#1e1e2e",
                                  highlightthickness=1,
                                  highlightbackground="#333")
        self.startmenu_visible = False

        items = [
            ("💻  Terminal", "terminal"),
            ("📝  Notepad", "notepad"),
            ("📁  File Manager", "filemanager"),
            ("⚙️  Settings", "settings"),
            ("⛶  Fullscreen", "fullscreen"),
            ("❌  Exit MiniOS", "exit"),
        ]
        for label, cmd in items:
            btn = tk.Label(self.startmenu, text=label, bg="#1e1e2e",
                           fg="#ddd", anchor="w", padx=20, pady=10,
                           cursor="hand2", font=("Courier", 11))
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2e2e4e"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#1e1e2e"))
            btn.bind("<Button-1>", lambda e, c=cmd: self.menu_action(c))

    def toggle_startmenu(self):
        if self.startmenu_visible:
            self.close_startmenu()
        else:
            self.startmenu.place(x=5, rely=1, y=-45, width=220,
                                 height=270, anchor="sw")
            self.startmenu.lift()
            self.startmenu_visible = True

    def close_startmenu(self, event=None):
        if self.startmenu_visible:
            self.startmenu.place_forget()
            self.startmenu_visible = False

    def menu_action(self, cmd):
        self.close_startmenu()
        if cmd == "exit":
            self.root.quit()
        elif cmd == "fullscreen":
            self.fullscreen_cb()
        else:
            self.launch_app(cmd)

    # ================= WINDOW CREATE =================
    def launch_app(self, app_name):
        # Kalau sudah ada, fokuskan saja
        if app_name in self.windows:
            self.focus_window(app_name)
            return

        titles = {
            "terminal": "Terminal",
            "notepad": "Notepad",
            "filemanager": "File Manager",
            "settings": "Settings",
        }
        title = titles.get(app_name, app_name)

        win = tk.Toplevel(self.root, bg="#1e1e2e")
        win.title(title)
        win.geometry(f"600x400+{100 + len(self.windows)*30}+{80 + len(self.windows)*30}")
        win.overrideredirect(False)

        # Window chrome (title bar custom)
        chrome = tk.Frame(win, bg="#2a2a3e", height=32)
        chrome.pack(fill="x")
        chrome.pack_propagate(False)

        tk.Label(chrome, text=f"  {title}", bg="#2a2a3e", fg="#fff",
                 font=("Courier", 10, "bold")).pack(side="left", padx=5)

        btn_frame = tk.Frame(chrome, bg="#2a2a3e")
        btn_frame.pack(side="right", padx=5)

        tk.Button(btn_frame, text="−", bg="#f1c40f", fg="#000",
                  relief="flat", width=3, cursor="hand2",
                  command=lambda: self.minimize_window(app_name)
                  ).pack(side="left", padx=2)

        tk.Button(btn_frame, text="□", bg="#2ecc71", fg="#000",
                  relief="flat", width=3, cursor="hand2",
                  command=lambda: self.toggle_maximize(win, app_name)
                  ).pack(side="left", padx=2)

        tk.Button(btn_frame, text="×", bg="#e74c3c", fg="#fff",
                  relief="flat", width=3, cursor="hand2",
                  command=lambda: self.close_window(app_name)
                  ).pack(side="left", padx=2)

        # Body content per app
        content = tk.Frame(win, bg="#1e1e2e")
        content.pack(fill="both", expand=True)

        apps = {
            "terminal": TerminalApp,
            "notepad": NotepadApp,
            "filemanager": FileManagerApp,
            "settings": SettingsApp,
        }
        app_instance = apps[app_name](content)

        self.windows[app_name] = {
            "win": win, "content": content,
            "app": app_instance, "minimized": False,
            "maximized": False
        }

        self.add_taskbar_item(app_name, title)
        self.focus_window(app_name)

    # ================= WINDOW CONTROLS =================
    def focus_window(self, app_name):
        data = self.windows[app_name]
        data["win"].lift()
        if data["minimized"]:
            data["win"].deiconify()
            data["minimized"] = False

    def minimize_window(self, app_name):
        data = self.windows[app_name]
        data["win"].withdraw()
        data["minimized"] = True

    def toggle_maximize(self, win, app_name):
        data = self.windows[app_name]
        if data["maximized"]:
            win.geometry(data["prev_geom"])
            data["maximized"] = False
        else:
            data["prev_geom"] = win.geometry()
            win.state("zoomed")
            data["maximized"] = True

    def close_window(self, app_name):
        data = self.windows[app_name]
        data["win"].destroy()
        del self.windows[app_name]
        self.remove_taskbar_item(app_name)

    # ================= TASKBAR ITEMS =================
    def add_taskbar_item(self, app_name, title):
        if hasattr(self, f"task_{app_name}"):
            return
        btn = tk.Button(
            self.task_list, text=title, bg="#1e1e2e", fg="#ccc",
            relief="flat", font=("Courier", 9),
            padx=10, pady=4, cursor="hand2",
            command=lambda: self.focus_window(app_name)
        )
        btn.pack(side="left", padx=3, pady=5)
        setattr(self, f"task_{app_name}", btn)

    def remove_taskbar_item(self, app_name):
        if hasattr(self, f"task_{app_name}"):
            getattr(self, f"task_{app_name}").destroy()
            delattr(self, f"task_{app_name}")
