import os
import json
import time
import hashlib
import threading
import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys

# Try to enable high DPI awareness for sharper UI and better zoom/scaling on Windows
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

SNAPSHOT_FILE = "snapshot.json"
FEEDBACK_FILE = "feedback.txt"

class FileIntegrityMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("CyberMon - File Integrity Dashboard")
        self.root.geometry("1100x700")

        self.selected_folder = ""
        self.monitoring = False
        self.snapshot = {}

        self.total_files = tk.StringVar(value="0")
        self.added_files = tk.StringVar(value="0")
        self.modified_files = tk.StringVar(value="0")
        self.deleted_files = tk.StringVar(value="0")
        self.status_text = tk.StringVar(value="Status: Ready")
        
        self.bg_widgets = []
        self.panel_widgets = []
        self.text_widgets = []
        self.muted_widgets = []
        self.current_theme = "idle"
        self.is_dark_mode = True

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.setup_styles()
        self.create_ui()
        self.set_theme("idle")

    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        self.btn_theme.config(text="☀️ Light" if self.is_dark_mode else "🌙 Dark")
        self.set_theme(self.current_theme)

    def set_theme(self, state):
        self.current_theme = state
        
        if self.is_dark_mode:
            if state == "scanning":
                bg_color = "#7f1d1d"
                panel_bg = "#450a0a"
                text_color = "#fef2f2"
                text_muted = "#fca5a5"
            else:
                bg_color = "#064e3b"
                panel_bg = "#022c22"
                text_color = "#ecfdf5"
                text_muted = "#6ee7b7"
        else:
            if state == "scanning":
                bg_color = "#fee2e2"
                panel_bg = "#fecaca"
                text_color = "#450a0a"
                text_muted = "#7f1d1d"
            else:
                bg_color = "#ecfdf5"
                panel_bg = "#d1fae5"
                text_color = "#022c22"
                text_muted = "#064e3b"

        self.root.configure(bg=bg_color)
        
        for w in self.bg_widgets:
            w.configure(bg=bg_color)
        for w in self.panel_widgets:
            w.configure(bg=panel_bg)
        for w in self.text_widgets:
            w.configure(fg=text_color, bg=w.cget('bg'))
        for w in self.muted_widgets:
            w.configure(fg=text_muted, bg=w.cget('bg'))

        style = ttk.Style(self.root)
        style.configure("Treeview", 
                        background=panel_bg,
                        foreground=text_color,
                        fieldbackground=panel_bg,
                        bordercolor=bg_color)
        
        style.configure("Treeview.Heading", 
                        background=bg_color,
                        foreground=text_muted,
                        bordercolor=bg_color)
        
        style.map("Treeview.Heading", background=[("active", bg_color)])

    def setup_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Treeview", borderwidth=0, rowheight=35, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", relief="flat", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#3b82f6")])

    def create_ui(self):
        header_frame = tk.Frame(self.root)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        self.bg_widgets.append(header_frame)

        title = tk.Label(header_frame, text="Dashboard Overview", font=("Segoe UI", 24, "bold"))
        title.pack(side="left")
        self.bg_widgets.append(title)
        self.text_widgets.append(title)

        self.btn_theme = tk.Button(header_frame, text="☀️ Light", command=self.toggle_dark_mode,
                                   bg="#64748b", fg="white", activebackground="#475569", activeforeground="white",
                                   font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=5, cursor="hand2")
        self.btn_theme.pack(side="right")

        control_panel = tk.Frame(self.root, padx=15, pady=15, bd=0)
        control_panel.pack(fill="x", padx=20, pady=10)
        self.panel_widgets.append(control_panel)

        self.folder_label = tk.Label(control_panel, text="No folder selected", font=("Segoe UI", 11))
        self.folder_label.pack(side="left", padx=10)
        self.panel_widgets.append(self.folder_label)
        self.muted_widgets.append(self.folder_label)

        btn_exit = tk.Button(control_panel, text="Exit Dashboard", command=self.on_closing,
                             bg="#475569", fg="white", activebackground="#334155", activeforeground="white",
                             font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=8, cursor="hand2")
        btn_exit.pack(side="right", padx=5)

        btn_stop = tk.Button(control_panel, text="Stop Monitoring", command=self.stop_monitor,
                             bg="#ef4444", fg="white", activebackground="#dc2626", activeforeground="white",
                             font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=8, cursor="hand2")
        btn_stop.pack(side="right", padx=5)

        self.btn_start = tk.Button(control_panel, text="Start Monitoring", command=self.start_monitor,
                              bg="#3b82f6", fg="white", activebackground="#2563eb", activeforeground="white",
                              font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=8, cursor="hand2")
        self.btn_start.pack(side="right", padx=5)

        btn_browse = tk.Button(control_panel, text="Browse Folder", command=self.select_folder,
                               bg="#334155", fg="white", activebackground="#475569", activeforeground="white",
                               font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=8, cursor="hand2")
        btn_browse.pack(side="right", padx=5)

        stats_frame = tk.Frame(self.root)
        stats_frame.pack(fill="x", padx=15, pady=10)
        self.bg_widgets.append(stats_frame)
        
        for i in range(4):
            stats_frame.columnconfigure(i, weight=1)

        self.create_stat_card(stats_frame, "Total Files", self.total_files, "#3b82f6", 0)
        self.create_stat_card(stats_frame, "Added", self.added_files, "#10b981", 1)
        self.create_stat_card(stats_frame, "Modified", self.modified_files, "#f59e0b", 2)
        self.create_stat_card(stats_frame, "Deleted", self.deleted_files, "#ef4444", 3)

        status_bar = tk.Frame(self.root)
        status_bar.pack(fill="x", padx=20, pady=5)
        self.bg_widgets.append(status_bar)
        
        status_lbl = tk.Label(status_bar, textvariable=self.status_text, font=("Segoe UI", 11, "bold"))
        status_lbl.pack(side="left")
        self.bg_widgets.append(status_lbl)
        self.text_widgets.append(status_lbl)

        table_frame = tk.Frame(self.root, padx=10, pady=10)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        self.panel_widgets.append(table_frame)

        table_title = tk.Label(table_frame, text="Recent Events", font=("Segoe UI", 14, "bold"))
        table_title.pack(anchor="w", pady=(0, 10))
        self.panel_widgets.append(table_title)
        self.text_widgets.append(table_title)

        columns = ("Event", "File Name", "Time")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        self.tree.heading("Event", text="EVENT TYPE")
        self.tree.heading("File Name", text="FILE PATH")
        self.tree.heading("Time", text="TIMESTAMP")

        self.tree.column("Event", width=150, anchor="center")
        self.tree.column("File Name", width=500, anchor="w")
        self.tree.column("Time", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.tag_configure("Added", foreground="#10b981")
        self.tree.tag_configure("Modified", foreground="#f59e0b")
        self.tree.tag_configure("Deleted", foreground="#ef4444")
        
        btn_bot = tk.Button(self.root, text="💬", command=self.open_bot,
                            bg="#8b5cf6", fg="white", activebackground="#7c3aed", activeforeground="white",
                            font=("Segoe UI", 24), bd=0, padx=15, pady=5, cursor="hand2")
        btn_bot.place(relx=1.0, rely=1.0, x=-30, y=-30, anchor="se")

    def create_stat_card(self, parent, title, variable, accent_color, column):
        card = tk.Frame(parent, padx=20, pady=20)
        card.grid(row=0, column=column, sticky="nsew", padx=5)
        self.panel_widgets.append(card)

        title_lbl = tk.Label(card, text=title.upper(), font=("Segoe UI", 10, "bold"))
        title_lbl.pack(anchor="w")
        self.panel_widgets.append(title_lbl)
        self.muted_widgets.append(title_lbl)

        val_lbl = tk.Label(card, textvariable=variable, fg=accent_color, font=("Segoe UI", 28, "bold"))
        val_lbl.pack(anchor="w", pady=(5, 0))
        self.panel_widgets.append(val_lbl)

    def open_bot(self):
        bot_win = tk.Toplevel(self.root)
        bot_win.title("CyberMon AI Assistant")
        bot_win.geometry("450x550")
        
        if self.is_dark_mode:
            bg_color = "#7f1d1d" if self.current_theme == "scanning" else "#064e3b"
            panel_bg = "#450a0a" if self.current_theme == "scanning" else "#022c22"
            text_color = "#fef2f2" if self.current_theme == "scanning" else "#ecfdf5"
        else:
            bg_color = "#fee2e2" if self.current_theme == "scanning" else "#ecfdf5"
            panel_bg = "#fecaca" if self.current_theme == "scanning" else "#d1fae5"
            text_color = "#450a0a" if self.current_theme == "scanning" else "#022c22"
            
        bot_win.configure(bg=bg_color)
        
        chat_frame = tk.Frame(bot_win, bg=panel_bg, padx=10, pady=10)
        chat_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        input_frame = tk.Frame(chat_frame, bg=panel_bg)
        input_frame.pack(side="bottom", fill="x")
        
        chat_log = tk.Text(chat_frame, bg=panel_bg, fg=text_color, font=("Segoe UI", 10), 
                           wrap="word", bd=0, state="disabled")
        chat_log.pack(side="top", fill="both", expand=True, pady=(0, 10))
        
        def append_message(sender, message, color):
            chat_log.config(state="normal")
            chat_log.insert("end", f"{sender}: ", "sender")
            chat_log.insert("end", f"{message}\n\n", "msg")
            chat_log.tag_config("sender", font=("Segoe UI", 10, "bold"), foreground=color)
            chat_log.tag_config("msg", foreground=text_color)
            chat_log.see("end")
            chat_log.config(state="disabled")

        append_message("Bot", "Hello! I am your CyberMon Assistant. Need a 'narration' of how things work? Or do you have some 'feedback' for us?", "#8b5cf6")

        entry = tk.Entry(input_frame, font=("Segoe UI", 11), bg=bg_color, fg=text_color, bd=0, insertbackground=text_color)
        entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        
        def process_input(event=None):
            user_text = entry.get().strip()
            if not user_text:
                return
            
            append_message("You", user_text, "#3b82f6")
            entry.delete(0, tk.END)
            
            lower_text = user_text.lower()
            if any(word in lower_text for word in ["how", "work", "explain", "narration", "help"]):
                narration = (
                    "Here's how this application works:\n"
                    "1. Click 'Browse Folder' to select a directory to monitor.\n"
                    "2. Click 'Start Monitoring'. I will take a snapshot of all files and their hashes.\n"
                    "3. Every 5 seconds, I will re-scan the folder and compare it against the snapshot.\n"
                    "4. Any added, modified, or deleted files will show up instantly on your dashboard!\n"
                    "5. The entire dashboard turns RED while actively scanning to keep you alert."
                )
                bot_win.after(500, lambda: append_message("Bot", narration, "#8b5cf6"))
            else:
                bot_win.after(500, lambda: append_message("Bot", "Thank you for the feedback! I've saved it to our feedback log.", "#8b5cf6"))
                with open(FEEDBACK_FILE, "a") as f:
                    f.write(f"[{datetime.datetime.now()}] {user_text}\n")

        entry.bind("<Return>", process_input)
        
        send_btn = tk.Button(input_frame, text="Send", command=process_input,
                             bg="#8b5cf6", fg="white", activebackground="#7c3aed", activeforeground="white",
                             font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=8, cursor="hand2")
        send_btn.pack(side="right")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder = folder
            self.folder_label.config(text=f"Target: {folder}")
            if self.folder_label in self.muted_widgets:
                self.muted_widgets.remove(self.folder_label)
                self.text_widgets.append(self.folder_label)
                self.set_theme("scanning" if self.monitoring else "idle")

    def file_hash(self, path):
        sha = hashlib.sha256()
        try:
            with open(path, "rb") as f:
                while True:
                    data = f.read(4096)
                    if not data:
                        break
                    sha.update(data)
            return sha.hexdigest()
        except:
            return ""

    def create_snapshot(self):
        snapshot = {}
        total = 0
        for root, dirs, files in os.walk(self.selected_folder):
            for file in files:
                path = os.path.join(root, file)
                snapshot[path] = self.file_hash(path)
                total += 1
        
        self.root.after(0, lambda: self.total_files.set(str(total)))
        return snapshot

    def start_monitor(self):
        if not self.selected_folder:
            messagebox.showerror("Error", "Select Folder First")
            return

        if self.monitoring:
            return

        self.monitoring = True
        self.status_text.set("Status: Initializing...")
        self.btn_start.config(state="disabled")
        
        self.set_theme("scanning")

        def init_task():
            self.snapshot = self.create_snapshot()
            with open(SNAPSHOT_FILE, "w") as f:
                json.dump(self.snapshot, f)
            
            self.root.after(0, lambda: self.status_text.set("Status: Monitoring Active"))
            self.monitor()

        thread = threading.Thread(target=init_task)
        thread.daemon = True
        thread.start()

    def stop_monitor(self):
        if not self.monitoring:
            return
        self.monitoring = False
        self.status_text.set("Status: Monitoring Stopped")
        self.btn_start.config(state="normal")
        
        self.set_theme("idle")

    def monitor(self):
        def loop():
            while self.monitoring:
                time.sleep(5)
                if not self.monitoring:
                    break
                new_snapshot = self.create_snapshot()
                self.compare(self.snapshot, new_snapshot)
                self.snapshot = new_snapshot
                try:
                    with open(SNAPSHOT_FILE, "w") as f:
                        json.dump(self.snapshot, f)
                except:
                    pass
        
        thread = threading.Thread(target=loop)
        thread.daemon = True
        thread.start()

    def compare(self, old, new):
        old_files = set(old.keys())
        new_files = set(new.keys())

        added = new_files - old_files
        deleted = old_files - new_files
        modified = []

        for file in old_files & new_files:
            if old[file] != new[file]:
                modified.append(file)

        current = datetime.datetime.now().strftime("%H:%M:%S")
        
        self.root.after(0, lambda: self.update_ui_stats(added, modified, deleted, current))

    def update_ui_stats(self, added, modified, deleted, current):
        self.added_files.set(str(len(added)))
        self.modified_files.set(str(len(modified)))
        self.deleted_files.set(str(len(deleted)))

        for file in added:
            self.tree.insert("", 0, values=("ADDED", file, current), tags=("Added",))
        for file in modified:
            self.tree.insert("", 0, values=("MODIFIED", file, current), tags=("Modified",))
        for file in deleted:
            self.tree.insert("", 0, values=("DELETED", file, current), tags=("Deleted",))

    def on_closing(self):
        """Safely shutdown background threads when closing the window."""
        self.monitoring = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileIntegrityMonitor(root)
    root.mainloop()