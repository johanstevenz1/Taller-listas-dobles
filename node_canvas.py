"""NodeCanvas class: draws the linked list (nodes and pointers) on a canvas."""

import tkinter as tk
from tkinter import ttk, font as tkfont

from theme import (DARK, ACCENT, RED, GREEN, MUTED, BORDER, CARD,
                   NODE_PENDING_FILL, NODE_PENDING_BORDER,
                   NODE_DONE_FILL, NODE_DONE_BORDER, scaled)

CANVAS_BG = "#FAFBFF"
DOT_COLOR = "#E3E7F4"


class NodeCanvas(tk.Frame):
    def __init__(self, parent, font_family="Helvetica", scale=1.0, **kwargs):
        super().__init__(parent, **kwargs)
        s = self.s = lambda n: scaled(n, scale)
        self.font_family = font_family
        self.height = s(128)
        self.data_width = s(172)
        self.pointer_width = s(38)
        self.gap = s(58)
        self.top = s(48)
        self.box_height = s(52)
        self.node_font = tkfont.Font(family=font_family, size=10, weight="bold")
        self._content_width = 0

        self.canvas = tk.Canvas(self, height=self.height, bg=CANVAS_BG,
                                highlightthickness=s(1),
                                highlightbackground=BORDER)
        scrollbar = ttk.Scrollbar(self, orient="horizontal",
                                  command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=scrollbar.set)
        self.canvas.pack(fill="x")
        scrollbar.pack(fill="x", pady=(s(4), 0))
        self.canvas.bind("<Configure>", lambda e: self._draw_dots())

    # ---------- drawing helpers ----------
    def _draw_dots(self):
        """Faint dotted background (crisp 1-pixel-aligned squares)."""
        c, s = self.canvas, self.s
        c.delete("dots")
        width = max(self._content_width, c.winfo_width())
        step, size = s(24), max(1, s(2))
        for x in range(step // 2, width, step):
            for y in range(step // 2, self.height, step):
                c.create_rectangle(x, y, x + size, y + size, fill=DOT_COLOR,
                                   outline="", tags="dots")
        c.tag_lower("dots")

    def _rounded_rect(self, x1, y1, x2, y2, radius=None, **options):
        r = radius if radius is not None else self.s(9)
        points = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
                  x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
                  x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
        return self.canvas.create_polygon(points, smooth=True, **options)

    def _fit(self, text, max_pixels):
        """Shorten the text with '...' so it fits inside the node."""
        if self.node_font.measure(text) <= max_pixels:
            return text
        while text and self.node_font.measure(text + "...") > max_pixels:
            text = text[:-1]
        return text + "..."

    def _head_tag(self, x, y):
        """Purple 'head' label with an arrow pointing to the first node."""
        c, s = self.canvas, self.s
        self._rounded_rect(x, y, x + s(58), y + s(24), radius=s(8),
                           fill=ACCENT, outline=ACCENT)
        c.create_text(x + s(29), y + s(12), text="head", fill="white",
                      font=(self.font_family, 9, "bold"))
        c.create_line(x + s(29), y + s(24), x + s(29), self.top - s(3),
                      arrow="last", width=s(2), fill=ACCENT,
                      arrowshape=(s(8), s(10), s(4)))

    # ---------- main drawing ----------
    def draw(self, linked_list, selected=None):
        c, s, family = self.canvas, self.s, self.font_family
        c.delete("all")

        if linked_list.is_empty():
            self._head_tag(s(20), s(10))
            top, bottom = self.top, self.top + self.box_height
            self._rounded_rect(s(20), top, s(20) + s(72), bottom, radius=s(8),
                               fill="#FBE9E7", outline=RED, width=s(2))
            c.create_text(s(20) + s(36), (top + bottom) / 2, text="None",
                          fill=RED, font=(family, 10, "bold"))
            c.create_text(s(120), (top + bottom) / 2, anchor="w",
                          text="The list is empty. Add a task to create the first node.",
                          font=(family, 10), fill=MUTED)
            self._content_width = 0
            c.configure(scrollregion=(0, 0, s(300), self.height))
            self._draw_dots()
            return

        x = s(20)
        self._head_tag(x, s(10))
        node_width = self.data_width + self.pointer_width
        top, bottom = self.top, self.top + self.box_height
        mid = (top + bottom) / 2

        for i, node in enumerate(linked_list):
            is_selected = i == selected
            fill = NODE_DONE_FILL if node.completed else NODE_PENDING_FILL
            border = (ACCENT if is_selected else
                      NODE_DONE_BORDER if node.completed else NODE_PENDING_BORDER)
            width = s(3) if is_selected else s(2)

            # shadow + node body
            self._rounded_rect(x + s(3), top + s(4), x + node_width + s(3),
                               bottom + s(4), fill="#DDE2F2", outline="")
            self._rounded_rect(x, top, x + node_width, bottom, fill=fill,
                               outline=border, width=width)

            # divider between data and pointer areas
            px = x + self.data_width
            c.create_line(px, top + s(6), px, bottom - s(6), fill=border,
                          width=s(1))

            # task text
            label = self._fit(node.task, self.data_width - s(20))
            if node.completed:
                label = "\u2713 " + label
            c.create_text(x + self.data_width / 2, mid, text=label,
                          font=self.node_font,
                          fill=GREEN if node.completed else DARK)

            # pointer dot
            cx = px + self.pointer_width / 2
            r = s(4)
            c.create_oval(cx - r, mid - r, cx + r, mid + r, fill=DARK,
                          outline="")

            # node number
            c.create_text(x + node_width / 2, bottom + s(17),
                          text=f"node {i + 1}",
                          fill=ACCENT if is_selected else MUTED,
                          font=(family, 8, "bold" if is_selected else "normal"))

            # arrow to the next node (or to None)
            end_x = x + node_width
            arrow = (s(10), s(12), s(4))
            if node.next is not None:
                c.create_line(cx, mid, end_x + self.gap, mid, arrow="last",
                              width=s(2), fill=DARK, arrowshape=arrow)
                x = end_x + self.gap
            else:
                c.create_line(cx, mid, end_x + s(30), mid, arrow="last",
                              width=s(2), fill=DARK, arrowshape=arrow)
                self._rounded_rect(end_x + s(34), mid - s(14), end_x + s(90),
                                   mid + s(14), radius=s(8), fill="#FBE9E7",
                                   outline=RED, width=s(2))
                c.create_text(end_x + s(62), mid, text="None", fill=RED,
                              font=(family, 10, "bold"))
                x = end_x + s(96)

        self._content_width = x + s(20)
        c.configure(scrollregion=(0, 0, self._content_width, self.height))
        self._draw_dots()
