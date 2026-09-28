"""Reusable visual widgets: Card (with shadow) and GradientHeader."""

import tkinter as tk
from tkinter import font as tkfont

from theme import (CARD, SHADOW, DARK, ACCENT, ORANGE, SOFT,
                   GRADIENT_START, GRADIENT_END, blend, scaled)


class Card(tk.Frame):
    """White panel with a soft shadow, an accent bar and a title.

    Put your widgets inside `card.content`. Extra widgets for the right side
    of the title row can go inside `card.header_right`.
    """

    def __init__(self, parent, title, font_family, scale=1.0, accent=ACCENT):
        super().__init__(parent, bg=SHADOW)
        s = lambda n: scaled(n, scale)
        inner = tk.Frame(self, bg=CARD)
        inner.pack(fill="both", expand=True, padx=s(1), pady=(s(1), s(3)))

        top = tk.Frame(inner, bg=CARD)
        top.pack(fill="x", padx=s(16), pady=(s(10), s(5)))
        tk.Frame(top, bg=accent, width=s(4), height=s(16)).pack(
            side="left", padx=(0, s(8)))
        tk.Label(top, text=title, bg=CARD, fg=DARK,
                 font=(font_family, 11, "bold")).pack(side="left")
        self.header_right = tk.Frame(top, bg=CARD)
        self.header_right.pack(side="right")

        self.content = tk.Frame(inner, bg=CARD)
        self.content.pack(fill="both", expand=True, padx=s(16), pady=(0, s(12)))


class GradientHeader(tk.Canvas):
    """Top banner with a gradient background, a logo, the title and counters."""

    def __init__(self, parent, font_family, scale=1.0):
        self.s = lambda n: scaled(n, scale)
        self.header_height = self.s(88)
        super().__init__(parent, height=self.header_height,
                         highlightthickness=0, bd=0, bg=GRADIENT_START)
        self.family = font_family
        self.stats = (0, 0, 0)
        self._last_width = 0
        self.bind("<Configure>", self._on_configure)

    def set_stats(self, total, pending, done):
        self.stats = (total, pending, done)
        self._draw()

    def _on_configure(self, event):
        if event.width != self._last_width:
            self._last_width = event.width
            self._draw()

    def _draw(self):
        s, f = self.s, self.family
        width = self.winfo_width()
        if width <= 1:
            return
        h = self.header_height
        self.delete("all")

        # gradient background
        step = s(3)
        for x in range(0, width, step):
            color = blend(GRADIENT_START, GRADIENT_END, x / width)
            self.create_rectangle(x, 0, x + step, h, fill=color, outline="")

        # logo: three linked nodes
        size = s(52)
        lx, ly = s(24), (h - size) // 2
        self.create_rectangle(lx, ly, lx + size, ly + size,
                              fill=blend(GRADIENT_START, "#FFFFFF", 0.12),
                              outline=blend(GRADIENT_START, "#FFFFFF", 0.30),
                              width=s(1))
        box = s(12)
        cy = ly + size // 2
        xs = [lx + s(5), lx + s(20), lx + s(35)]
        for i, bx in enumerate(xs):
            self.create_rectangle(bx, cy - box // 2, bx + box, cy + box // 2,
                                  fill="white", outline="")
            if i < 2:
                self.create_line(bx + box, cy, xs[i + 1], cy, fill=ORANGE,
                                 width=s(2))

        # badge + title + subtitle
        tx = lx + size + s(16)
        badge = self.create_text(tx + s(9), s(18), anchor="w",
                                 text="SINGLY LINKED LISTS", fill="white",
                                 font=(f, 8, "bold"))
        x1, y1, x2, y2 = self.bbox(badge)
        rect = self.create_rectangle(x1 - s(9), y1 - s(3), x2 + s(9), y2 + s(3),
                                     fill=ORANGE, outline="")
        self.tag_lower(rect, badge)
        self.create_text(tx, s(46), anchor="w", text="To-do list",
                         fill="white", font=(f, 21, "bold"))
        self.create_text(tx, s(71), anchor="w",
                         text="Every task is a node that points to the next one.",
                         fill=SOFT, font=(f, 10))

        # counters on the right
        chip_w, chip_h, gap = s(92), s(60), s(10)
        total, pending, done = self.stats
        chips = [(str(total), "TOTAL", "#FFFFFF"),
                 (str(pending), "PENDING", "#FFB08A"),
                 (str(done), "DONE", "#7BE0A5")]
        x = width - s(24) - len(chips) * chip_w - (len(chips) - 1) * gap
        top = (h - chip_h) // 2
        for value, label, color in chips:
            self.create_rectangle(x, top, x + chip_w, top + chip_h,
                                  fill="#2C3384", outline="#4F57AE",
                                  width=s(1))
            self.create_rectangle(x, top, x + chip_w, top + s(4),
                                  fill=color, outline="")
            self.create_text(x + chip_w / 2, top + s(26), text=value,
                             fill=color, font=(f, 19, "bold"))
            self.create_text(x + chip_w / 2, top + s(48), text=label,
                             fill=SOFT, font=(f, 8, "bold"))
            x += chip_w + gap
