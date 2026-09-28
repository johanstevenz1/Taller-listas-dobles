"""Entry point. Run with:  python main.py"""

import tkinter as tk

from task_app import TaskApp
from theme import enable_high_dpi


def main():
    enable_high_dpi()   # must run BEFORE creating the window (sharp text on Windows)
    root = tk.Tk()
    TaskApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
