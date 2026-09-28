"""Shared colors and display helpers (sharpness / DPI scaling / fonts)."""

import sys
import tkinter as tk
from tkinter import font as tkfont

# ---------- color palette ----------
BACKGROUND = "#EEF1F9"
CARD = "#FFFFFF"
BORDER = "#DCE2F0"
SHADOW = "#D3D9EB"
DARK = "#1F2557"
ACCENT = "#8A2E8F"
ACCENT_DARK = "#6E2372"
ORANGE = "#FF7B47"
GREEN = "#2E8B57"
GREEN_DARK = "#256F46"
RED = "#D64545"
RED_DARK = "#B93636"
MUTED = "#6B7390"
SOFT = "#B9BFE6"
ROW_ODD = "#F7F9FE"
GRADIENT_START = "#1B2154"
GRADIENT_END = "#6A2B85"

# node colors (used by the canvas and its legend)
NODE_PENDING_FILL = "#EEF0FF"
NODE_PENDING_BORDER = "#B8C0E0"
NODE_DONE_FILL = "#E3F6EA"
NODE_DONE_BORDER = "#7FC79B"


def enable_high_dpi():
    """Ask Windows not to blur the window on high-resolution screens.

    Must be called BEFORE creating the Tk window. Does nothing on other systems.
    """
    if sys.platform != "win32":
        return
    try:
        import ctypes
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # per-monitor DPI
        except Exception:
            ctypes.windll.user32.SetProcessDPIAware()       # older Windows
    except Exception:
        pass


def get_scale(root):
    """Scale factor for pixel sizes (1.0 = 96 dpi). Only needed on Windows,
    where fonts scale automatically but pixel sizes do not."""
    if sys.platform == "win32":
        try:
            return max(1.0, root.winfo_fpixels("1i") / 96.0)
        except tk.TclError:
            return 1.0
    return 1.0


def scaled(value, scale):
    """Convert a size in 'design pixels' to real pixels."""
    return int(round(value * scale))


def pick_font_family(root):
    """Choose the nicest font available on the current system."""
    available = set(tkfont.families(root))
    for name in ("Segoe UI", "SF Pro Text", "Helvetica Neue", "Helvetica",
                 "DejaVu Sans", "Arial"):
        if name in available:
            return name
    return "Helvetica"


def blend(color_a, color_b, t):
    """Linear mix of two '#rrggbb' colors (t=0 -> a, t=1 -> b)."""
    a = [int(color_a[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(color_b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(x + (y - x) * t) for x, y in zip(a, b))
