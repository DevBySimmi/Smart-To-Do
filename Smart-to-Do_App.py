import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime


DATA_FILE = "tasks.json"

# =========================
# Colors
# =========================

BG = "#FFF7FB"
CARD = "#FFFFFF"
PINK = "#FF8FB3"
DARK_PINK = "#E96B96"
PURPLE = "#A78BFA"
TEXT = "#493B47"
LIGHT_PINK = "#FFE4EF"
LIGHT_PURPLE = "#EEE8FF"
GREEN = "#75C9A3"
LIGHT_GREEN = "#E2F7EC"
RED = "#F28B82"
LIGHT_RED = "#FFE4E2"


class SmartTodo:

    def __init__(self, root):
        self.root = root

        self.root.title("🌸 Smart To-Do")
        self.root.geometry("900x680")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.tasks = []
        self.load_tasks()

        self.setup_style()
        self.create_ui()
        self.refresh_tasks()

    # =========================
    # Style
    # =========================

    def setup_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "Cute.TCombobox",
            fieldbackground="white",
            background="white",
            foreground=TEXT
        )

        style.configure(
            "Cute.Treeview",
            background=CARD,
            foreground=TEXT,
            fieldbackground=CARD,
            rowheight=38,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Cute.Treeview.Heading",
            background=LIGHT_PINK,
            foreground=TEXT,
            font=("Segoe UI", 10, "bold")
        )

    # =========================
    # Load Tasks
    # =========================

    def load_tasks(self):

        if os.path.exists(DATA_FILE):

            try:
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    self.tasks = json.load(file)

            except:
                self.tasks = []

    # =========================
    # Save Tasks
    # =========================

    def save_tasks(self):

        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(
                self.tasks,
                file,
                indent=4,
                ensure_ascii=False
            )

    # =========================
    # Main UI
    # =========================

    def create_ui(self):

        # Header
        header = tk.Frame(
            self.root,
            bg=BG
        )
        header.pack(fill="x", pady=(25, 5))

        tk.Label(
            header,
            text="🌸 SMART TO-DO 🌸",
            font=("Segoe UI", 27, "bold"),
            bg=BG,
            fg=DARK_PINK
        ).pack()

        tk.Label(
            header,
            text="✨ Plan it • Do it • Feel proud ✨",
            font=("Segoe UI", 11),
            bg=BG,
            fg=TEXT
        ).pack(pady=(3, 0))

        # =========================
        # Add Task Card
        # =========================

        card = tk.Frame(
            self.root,
            bg=CARD,
            highlightbackground="#F4D6E3",
            highlightthickness=1
        )
        card.pack(
            fill="x",
            padx=35,
            pady=18
        )

        tk.Label(
            card,
            text="💗 Add a New Task",
            font=("Segoe UI", 13, "bold"),
            bg=CARD,
            fg=DARK_PINK
        ).grid(
            row=0,
            column=0,
            columnspan=7,
            sticky="w",
            padx=20,
            pady=(15, 10)
        )

        # Task
        tk.Label(
            card,
            text="Task",
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI", 9, "bold")
        ).grid(row=1, column=0, padx=(20, 5))

        self.task_entry = tk.Entry(
            card,
            width=28,
            font=("Segoe UI", 10),
            bg="#FFF9FC",
            fg=TEXT,
            relief="flat",
            highlightbackground="#F1C9DA",
            highlightthickness=1
        )
        self.task_entry.grid(
            row=1,
            column=1,
            padx=5,
            ipady=7
        )

        # Priority
        tk.Label(
            card,
            text="Priority",
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI", 9, "bold")
        ).grid(row=1, column=2, padx=5)

        self.priority_box = ttk.Combobox(
            card,
            values=["Low", "Medium", "High"],
            state="readonly",
            width=10,
            style="Cute.TCombobox"
        )
        self.priority_box.set("Medium")
        self.priority_box.grid(row=1, column=3, padx=5)

        # Date
        tk.Label(
            card,
            text="Due",
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI", 9, "bold")
        ).grid(row=1, column=4, padx=5)

        self.date_entry = tk.Entry(
            card,
            width=12,
            font=("Segoe UI", 10),
            bg="#FFF9FC",
            fg=TEXT,
            relief="flat",
            highlightbackground="#F1C9DA",
            highlightthickness=1
        )
        self.date_entry.insert(0, "DD-MM-YYYY")

        self.date_entry.grid(
            row=1,
            column=5,
            padx=5,
            ipady=7
        )

        # Add Button
        tk.Button(
            card,
            text="＋ Add",
            command=self.add_task,
            bg=PINK,
            fg="white",
            activebackground=DARK_PINK,
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7
        ).grid(
            row=1,
            column=6,
            padx=(5, 20)
        )

        # =========================
        # Search
        # =========================

        search_frame = tk.Frame(
            self.root,
            bg=BG
        )
        search_frame.pack(
            fill="x",
            padx=35,
            pady=(0, 10)
        )

        tk.Label(
            search_frame,
            text="🔍",
            bg=BG,
            fg=DARK_PINK,
            font=("Segoe UI", 14)
        ).pack(side="left")

        self.search_entry = tk.Entry(
            search_frame,
            width=50,
            font=("Segoe UI", 10),
            bg=CARD,
            fg=TEXT,
            relief="flat",
            highlightbackground="#EACDDA",
            highlightthickness=1
        )
        self.search_entry.pack(
            side="left",
            padx=8,
            ipady=7
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.refresh_tasks()
        )

        tk.Button(
            search_frame,
            text="Clear",
            command=self.clear_search,
            bg=LIGHT_PINK,
            fg=DARK_PINK,
            activebackground="#FFD1E2",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=6,
            cursor="hand2"
        ).pack(side="left")

        # =========================
        # Task List
        # =========================

        list_card = tk.Frame(
            self.root,
            bg=CARD,
            highlightbackground="#F4D6E3",
            highlightthickness=1
        )

        list_card.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=5
        )

        self.tree = ttk.Treeview(
            list_card,
            columns=(
                "task",
                "priority",
                "due",
                "status"
            ),
            show="headings",
            height=11,
            style="Cute.Treeview"
        )

        self.tree.heading(
            "task",
            text="💗 Task"
        )

        self.tree.heading(
            "priority",
            text="⭐ Priority"
        )

        self.tree.heading(
            "due",
            text="📅 Due"
        )

        self.tree.heading(
            "status",
            text="✨ Status"
        )

        self.tree.column(
            "task",
            width=390
        )

        self.tree.column(
            "priority",
            width=120,
            anchor="center"
        )

        self.tree.column(
            "due",
            width=130,
            anchor="center"
        )

        self.tree.column(
            "status",
            width=130,
            anchor="center"
        )

        self.tree.tag_configure(
            "completed",
            foreground="#8A7D87"
        )

        self.tree.tag_configure(
            "high",
            foreground="#D85B69"
        )

        self.tree.tag_configure(
            "medium",
            foreground="#B47B25"
        )

        self.tree.tag_configure(
            "low",
            foreground="#4E9B78"
        )

        scrollbar = ttk.Scrollbar(
            list_card,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0),
            pady=10
        )

        scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 10),
            pady=10
        )

        # =========================
        # Buttons
        # =========================

        button_frame = tk.Frame(
            self.root,
            bg=BG
        )
        button_frame.pack(pady=12)

        self.make_button(
            button_frame,
            "✓ Complete",
            GREEN,
            self.complete_task
        ).pack(side="left", padx=5)

        self.make_button(
            button_frame,
            "🗑 Delete",
            RED,
            self.delete_task
        ).pack(side="left", padx=5)

        self.make_button(
            button_frame,
            "↻ Refresh",
            PURPLE,
            self.refresh_tasks
        ).pack(side="left", padx=5)

        # =========================
        # Statistics
        # =========================

        self.stats_label = tk.Label(
            self.root,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg=BG,
            fg=TEXT
        )

        self.stats_label.pack(pady=(0, 18))

    # =========================
    # Cute Button
    # =========================

    def make_button(
        self,
        parent,
        text,
        color,
        command
    ):

        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=7,
            cursor="hand2"
        )

    # =========================
    # Add Task
    # =========================

    def add_task(self):

        task_name = self.task_entry.get().strip()
        priority = self.priority_box.get()
        due_date = self.date_entry.get().strip()

        if not task_name:

            messagebox.showwarning(
                "🌸 Oops!",
                "Please enter a task first 💗"
            )

            return

        if due_date != "DD-MM-YYYY":

            try:

                datetime.strptime(
                    due_date,
                    "%d-%m-%Y"
                )

            except ValueError:

                messagebox.showwarning(
                    "🌸 Invalid Date",
                    "Please use DD-MM-YYYY format."
                )

                return

        else:
            due_date = "No deadline"

        task = {
            "task": task_name,
            "priority": priority,
            "due": due_date,
            "completed": False
        }

        self.tasks.append(task)

        self.save_tasks()

        self.task_entry.delete(
            0,
            tk.END
        )

        self.date_entry.delete(
            0,
            tk.END
        )

        self.date_entry.insert(
            0,
            "DD-MM-YYYY"
        )

        self.refresh_tasks()

    # =========================
    # Complete
    # =========================

    def complete_task(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "🌸 Select a Task",
                "Please select a task first."
            )

            return

        index = int(selected[0])

        self.tasks[index]["completed"] = True

        self.save_tasks()
        self.refresh_tasks()

    # =========================
    # Delete
    # =========================

    def delete_task(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "🌸 Select a Task",
                "Please select a task first."
            )

            return

        index = int(selected[0])

        confirm = messagebox.askyesno(
            "🗑 Delete Task",
            "Are you sure you want to delete this task?"
        )

        if confirm:

            self.tasks.pop(index)

            self.save_tasks()
            self.refresh_tasks()

    # =========================
    # Search
    # =========================

    def clear_search(self):

        self.search_entry.delete(
            0,
            tk.END
        )

        self.refresh_tasks()

    # =========================
    # Refresh
    # =========================

    def refresh_tasks(self):

        for item in self.tree.get_children():

            self.tree.delete(item)

        search = ""

        if hasattr(
            self,
            "search_entry"
        ):

            search = (
                self.search_entry
                .get()
                .strip()
                .lower()
            )

        for index, task in enumerate(self.tasks):

            if search and search not in task["task"].lower():
                continue

            if task["completed"]:

                status = "✓ Completed"
                tag = "completed"

            else:

                status = "○ Pending"

                if task["priority"] == "High":
                    tag = "high"

                elif task["priority"] == "Medium":
                    tag = "medium"

                else:
                    tag = "low"

            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    task["task"],
                    task["priority"],
                    task["due"],
                    status
                ),
                tags=(tag,)
            )

        self.update_statistics()

    # =========================
    # Statistics
    # =========================

    def update_statistics(self):

        total = len(self.tasks)

        completed = sum(
            1
            for task in self.tasks
            if task["completed"]
        )

        pending = total - completed

        self.stats_label.config(
            text=(
                f"🌷 Total: {total}   •   "
                f"✓ Completed: {completed}   •   "
                f"○ Pending: {pending}   🌷"
            )
        )


# =========================
# Start App
# =========================

root = tk.Tk()

app = SmartTodo(root)

root.mainloop()