"""Node class: one node = one task + a reference to the next node."""


class Node:
    def __init__(self, task):
        self.task = task
        self.completed = False
        self.next = None  # pointer to the next node (None = end of the list)

    def __repr__(self):
        return f"Node({self.task!r}, completed={self.completed})"
