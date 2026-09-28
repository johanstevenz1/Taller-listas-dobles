"""TaskApp class: the frontend (Tkinter window) for the to-do linked list."""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from task_list import TaskLinkedList
from node_canvas import NodeCanvas
from widgets import Card, GradientHeader
from theme import (BACKGROUND, CARD, BORDER, DARK, ACCENT, ACCENT_DARK, GREEN,
                   GREEN_DARK, RED, RED_DARK, MUTED, ROW_ODD,
                   NODE_PENDING_BORDER, NODE_DONE_BORDER,
                   get_scale, scaled, pick_font_family)

STATUS_BAR = "#E4E8F4"


class TaskApp:
    def __init__(self, root):
        self.root = root
        self.tasks = TaskLinkedList()
        self.font = pick_font_family(root)
        self.scale = get_scale(root)
        self.px = lambda n: scaled(n, self.scale)
        px = self.px

        root.title("Singly Linked List Workshop - To-do list")
        root.configure(bg=BACKGROUND)

        self._setup_styles()
        self.header = GradientHeader(root, self.font, self.scale)
        self.header.pack(fill="x")
        self._build_status_bar()

        self.body = tk.Frame(root, bg=BACKGROUND)
        self.body.pack(fill="both", expand=True, padx=px(20), pady=(px(14), px(4)))
        self._build_node_view()      # packed at the bottom first, so it is never squeezed
        top = tk.Frame(self.body, bg=BACKGROUND)
        top.pack(fill="both", expand=True)
        sidebar = tk.Frame(top, bg=BACKGROUND)
        sidebar.pack(side="right", fill="y", padx=(px(14), 0))
        self._build_inputs(sidebar)
        self._build_buttons(sidebar)
        self._build_task_list(top)

        self._fit_window()
        for task in ("Study linked lists", "Do the Python workshop",
                     "Submit the project"):
            self.tasks.add_last(task)
        self.refresh()
        self.task_entry.focus_set()

    def _fit_window(self):
        """Size the window to its content, limited to the screen size."""
        px, root = self.px, self.root
        root.update_idletasks()
        max_w = root.winfo_screenwidth() - px(40)
        max_h = root.winfo_screenheight() - px(90)
        width = min(max(px(1040), root.winfo_reqwidth()), max_w)
        height = min(max(px(700), root.winfo_reqheight()), max_h)
        root.geometry(f"{width}x{height}")
        root.minsize(min(px(900), width), min(root.winfo_reqheight(), height))

    # ---------- styles ----------
    def _setup_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")  # the only built-in theme that accepts colors everywhere
        f, px = self.font, self.px

        def button(name, bg, hover, fg="white"):
            style.configure(name, background=bg, foreground=fg,
                            bordercolor=bg, lightcolor=bg, darkcolor=bg,
                            focuscolor=bg, focusthickness=0, borderwidth=px(1),
                            padding=(px(6), px(7)), font=(f, 9, "bold"),
                            relief="flat")
            style.map(name,
                      background=[("pressed", hover), ("active", hover)],
                      bordercolor=[("pressed", hover), ("active", hover)],
                      lightcolor=[("pressed", hover), ("active", hover)],
                      darkcolor=[("pressed", hover), ("active", hover)])

        button("Primary.TButton", ACCENT, ACCENT_DARK)
        button("Danger.TButton", RED, RED_DARK)
        button("Success.TButton", GREEN, GREEN_DARK)
        button("Secondary.TButton", "#E9ECF8", "#D8DCF0", fg=DARK)

        style.configure("TEntry", padding=px(8), fieldbackground="white",
                        bordercolor=BORDER, lightcolor=BORDER,
                        darkcolor=BORDER, insertcolor=DARK)
        style.map("TEntry", bordercolor=[("focus", ACCENT)],
                  lightcolor=[("focus", ACCENT)],
                  darkcolor=[("focus", ACCENT)])

        for orient in ("Vertical", "Horizontal"):
            style.configure(f"{orient}.TScrollbar", background="#D5DAEC",
                            troughcolor="#F1F4FA", bordercolor="#F1F4FA",
                            lightcolor="#D5DAEC", darkcolor="#D5DAEC",
                            arrowcolor=DARK, relief="flat",
                            arrowsize=px(14))

        style.configure("Tasks.Treeview", background=CARD,
                        fieldbackground=CARD, foreground=DARK,
                        rowheight=px(38), borderwidth=0, relief="flat",
                        font=(f, 12))
        style.map("Tasks.Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", "white")])
        style.configure("Tasks.Treeview.Heading", background="#EEF1FA",
                        foreground=MUTED, relief="flat", borderwidth=0,
                        padding=(px(10), px(7)), font=(f, 9, "bold"))
        style.map("Tasks.Treeview.Heading",
                  background=[("active", "#EEF1FA")])
        style.layout("Tasks.Treeview",
                     [("Treeview.treearea", {"sticky": "nswe"})])

    # ---------- layout ----------
    def _build_inputs(self, parent):
        f, px = self.font, self.px
        card = Card(parent, "New task", f, self.scale)
        card.pack(fill="x", pady=(0, px(8)))
        content = card.content
        content.columnconfigure(0, weight=1)
        tk.Label(content, text="Task", bg=CARD, fg=MUTED,
                 font=(f, 9, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(content, text="Position (1..n)", bg=CARD, fg=MUTED,
                 font=(f, 9, "bold")).grid(row=0, column=1, sticky="w",
                                           padx=(px(10), 0))
        self.task_entry = ttk.Entry(content, font=(f, 12))
        self.task_entry.grid(row=1, column=0, sticky="ew", pady=(px(3), 0))
        self.task_entry.bind("<Return>", lambda e: self.add_last())
        self.position_entry = ttk.Entry(content, width=7, font=(f, 12))
        self.position_entry.grid(row=1, column=1, sticky="w",
                                 padx=(px(10), 0), pady=(px(3), 0))

    def _build_buttons(self, parent):
        px = self.px
        card = Card(parent, "Actions", self.font, self.scale)
        card.pack(fill="x")
        content = card.content
        buttons = [
            ("\u2191  Add first", self.add_first, "Primary.TButton"),
            ("\u2193  Add last", self.add_last, "Primary.TButton"),
            ("+  Insert at position", self.insert_at_position, "Primary.TButton"),
            ("\u2715  Remove selected", self.remove_selected, "Danger.TButton"),
            ("\u2715  Remove first", self.remove_first, "Danger.TButton"),
            ("\u2714  Toggle done", self.toggle_completed, "Success.TButton"),
            ("\u270E  Edit", self.edit_selected, "Secondary.TButton"),
            ("\u2315  Search", self.search, "Secondary.TButton"),
            ("\u21C4  Reverse list", self.reverse, "Secondary.TButton"),
        ]
        for i, (text, command, style) in enumerate(buttons):
            ttk.Button(content, text=text, command=command, style=style,
                       cursor="hand2").grid(row=i // 3, column=i % 3,
                                            padx=px(3), pady=px(3),
                                            sticky="ew")
        for col in range(3):
            content.columnconfigure(col, weight=1, uniform="buttons")

    def _build_task_list(self, parent):
        f, px = self.font, self.px
        card = Card(parent, "Tasks", f, self.scale)
        card.pack(side="left", fill="both", expand=True)
        tk.Label(card.header_right,
                 text="Double-click a task to mark it as done",
                 bg=CARD, fg=MUTED, font=(f, 9)).pack()

        holder = card.content
        self.tree = ttk.Treeview(holder, columns=("num", "status", "task"),
                                 show="headings", selectmode="browse",
                                 style="Tasks.Treeview", height=6)
        self.tree.heading("num", text="#")
        self.tree.heading("status", text="STATUS", anchor="w")
        self.tree.heading("task", text="TASK", anchor="w")
        self.tree.column("num", width=px(56), minwidth=px(56), stretch=False,
                         anchor="center")
        self.tree.column("status", width=px(120), minwidth=px(100),
                         stretch=False, anchor="w")
        self.tree.column("task", width=px(300), anchor="w", stretch=True)
        self.tree.tag_configure("even", background=CARD)
        self.tree.tag_configure("odd", background=ROW_ODD)
        self.tree.tag_configure("done", foreground=GREEN)

        scrollbar = ttk.Scrollbar(holder, orient="vertical",
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-1>", self._on_double_click)
        self.tree.bind("<Delete>", lambda e: self.remove_selected())

        self.empty_label = tk.Label(
            holder, text="No tasks yet\nType a task and press Enter",
            bg=CARD, fg=MUTED, font=(f, 11), justify="center")

    def _build_node_view(self):
        f = self.font
        card = Card(self.body, "Linked list view (nodes and pointers)", f,
                    self.scale, accent="#FF7B47")
        card.pack(side="bottom", fill="x", pady=(self.px(10), 0))
        for color, text in ((NODE_PENDING_BORDER, "Pending"),
                            (NODE_DONE_BORDER, "Done"), (ACCENT, "Selected")):
            tk.Label(card.header_right, text="\u25A0", fg=color, bg=CARD,
                     font=(f, 11)).pack(side="left")
            tk.Label(card.header_right, text=text, fg=MUTED, bg=CARD,
                     font=(f, 9)).pack(side="left", padx=(2, 10))
        self.node_canvas = NodeCanvas(card.content, font_family=f,
                                      scale=self.scale, bg=CARD)
        self.node_canvas.pack(fill="x")

    def _build_status_bar(self):
        px = self.px
        bar = tk.Frame(self.root, bg=STATUS_BAR)
        bar.pack(side="bottom", fill="x")
        tk.Label(bar, text="\u25CF", bg=STATUS_BAR, fg=ACCENT,
                 font=(self.font, 10)).pack(side="left", padx=(px(20), px(6)),
                                            pady=px(8))
        self.status = tk.Label(bar, text="", anchor="w", bg=STATUS_BAR,
                               fg=ACCENT, font=(self.font, 10, "bold"))
        self.status.pack(side="left", fill="x")
        tk.Label(bar, text="Tip: select a task and press Delete to remove it",
                 bg=STATUS_BAR, fg=MUTED, font=(self.font, 9)
                 ).pack(side="right", padx=px(20))

    # ---------- view update ----------
    def refresh(self, selected=None, message=None):
        self.tree.delete(*self.tree.get_children())
        for i, node in enumerate(self.tasks):
            status = "\u2714  Done" if node.completed else "\u25CB  Pending"
            tags = ["odd" if i % 2 else "even"]
            if node.completed:
                tags.append("done")
            self.tree.insert("", tk.END, iid=str(i),
                             values=(i + 1, status, node.task), tags=tags)
        if selected is not None and 0 <= selected < len(self.tasks):
            self.tree.selection_set(str(selected))
            self.tree.see(str(selected))
        else:
            selected = None
        self.node_canvas.draw(self.tasks, selected)

        if self.tasks.is_empty():
            self.empty_label.place(in_=self.tree, relx=0.5, rely=0.5,
                                   anchor="center")
        else:
            self.empty_label.place_forget()

        total = len(self.tasks)
        pending = sum(1 for node in self.tasks if not node.completed)
        self.header.set_stats(total, pending, total - pending)
        prefix = f"{message}   |   " if message else ""
        self.status.config(text=f"{prefix}Total: {total} tasks - Pending: {pending}")

    def _on_select(self, _event):
        index = self._selected_index(silent=True)
        if index is not None:
            self.node_canvas.draw(self.tasks, index)

    def _on_double_click(self, event):
        if self.tree.identify_region(event.x, event.y) == "cell":
            self.toggle_completed()

    # ---------- input helpers ----------
    def _read_task(self):
        text = self.task_entry.get().strip()
        if not text:
            messagebox.showwarning("Missing task", "Type a task first.")
            return None
        return text

    def _selected_index(self, silent=False):
        selection = self.tree.selection()
        if not selection:
            if not silent:
                messagebox.showinfo("Select a task",
                                    "Select a task from the list first.")
            return None
        return int(selection[0])

    # ---------- actions ----------
    def add_first(self):
        task = self._read_task()
        if task:
            self.tasks.add_first(task)
            self.task_entry.delete(0, tk.END)
            self.refresh(0, "Added at the beginning")

    def add_last(self):
        task = self._read_task()
        if task:
            self.tasks.add_last(task)
            self.task_entry.delete(0, tk.END)
            self.refresh(len(self.tasks) - 1, "Added at the end")

    def insert_at_position(self):
        task = self._read_task()
        if not task:
            return
        try:
            position = int(self.position_entry.get()) - 1
            self.tasks.insert_at(position, task)
        except ValueError:
            messagebox.showerror("Invalid position",
                                 "Type a whole number in Position.")
            return
        except IndexError:
            messagebox.showerror(
                "Invalid position",
                f"Position must be between 1 and {len(self.tasks) + 1}.")
            return
        self.task_entry.delete(0, tk.END)
        self.refresh(position, f"Inserted at position {position + 1}")

    def remove_selected(self):
        index = self._selected_index()
        if index is not None:
            removed = self.tasks.remove_at(index)
            self.refresh(None, f"Removed: {removed}")

    def remove_first(self):
        if self.tasks.is_empty():
            messagebox.showinfo("Empty list", "There are no tasks to remove.")
            return
        removed = self.tasks.remove_at(0)
        self.refresh(None, f"Removed: {removed}")

    def toggle_completed(self):
        index = self._selected_index()
        if index is not None:
            done = self.tasks.toggle_completed(index)
            self.refresh(index, "Marked as done" if done else "Marked as pending")

    def edit_selected(self):
        index = self._selected_index()
        if index is None:
            return
        new_text = simpledialog.askstring(
            "Edit task", "New text:",
            initialvalue=self.tasks.get(index).task, parent=self.root)
        if new_text and new_text.strip():
            self.tasks.edit(index, new_text.strip())
            self.refresh(index, "Task edited")

    def search(self):
        text = self.task_entry.get().strip()
        if not text:
            messagebox.showwarning(
                "Search", "Type the text to search in the Task field.")
            return
        positions = self.tasks.search(text)
        if not positions:
            self.refresh(None, "No matches")
            return
        found = ", ".join(str(p + 1) for p in positions)
        self.refresh(positions[0], f"Matches at position: {found}")

    def reverse(self):
        self.tasks.reverse()
        self.refresh(None, "List reversed")
