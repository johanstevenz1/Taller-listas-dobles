"""TaskLinkedList class: a singly linked list of tasks (no Python list used)."""

from node import Node


class TaskLinkedList:
    """Singly linked list. It only keeps a reference to the head node."""

    def __init__(self):
        self.head = None
        self._size = 0

    # ---------- helpers ----------
    def is_empty(self):
        return self.head is None

    def __len__(self):
        return self._size

    def __iter__(self):
        """Traverse the list by following the `next` pointers."""
        current = self.head
        while current is not None:
            yield current
            current = current.next

    def _check_position(self, position, include_end=False):
        last_valid = self._size if include_end else self._size - 1
        if not 0 <= position <= last_valid:
            raise IndexError("Position out of range")

    # ---------- insertion ----------
    def add_first(self, task):
        new_node = Node(task)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def add_last(self, task):
        new_node = Node(task)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def insert_at(self, position, task):
        """Insert a task at the given position (0-based)."""
        self._check_position(position, include_end=True)
        if position == 0:
            self.add_first(task)
            return
        previous = self.head
        for _ in range(position - 1):
            previous = previous.next
        new_node = Node(task)
        new_node.next = previous.next
        previous.next = new_node
        self._size += 1

    # ---------- deletion ----------
    def remove_at(self, position):
        """Remove the node at the given position and return its task."""
        self._check_position(position)
        if position == 0:
            removed = self.head
            self.head = removed.next
        else:
            previous = self.head
            for _ in range(position - 1):
                previous = previous.next
            removed = previous.next
            previous.next = removed.next
        self._size -= 1
        return removed.task

    # ---------- query / update ----------
    def get(self, position):
        self._check_position(position)
        current = self.head
        for _ in range(position):
            current = current.next
        return current

    def search(self, text):
        """Return the positions of the tasks that contain the given text."""
        text = text.lower()
        return [i for i, node in enumerate(self) if text in node.task.lower()]

    def toggle_completed(self, position):
        node = self.get(position)
        node.completed = not node.completed
        return node.completed

    def edit(self, position, new_task):
        self.get(position).task = new_task

    def reverse(self):
        """Reverse the list by changing the direction of the pointers."""
        previous = None
        current = self.head
        while current is not None:
            following = current.next
            current.next = previous
            previous = current
            current = following
        self.head = previous
