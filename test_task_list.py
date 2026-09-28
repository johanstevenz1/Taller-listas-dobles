"""Unit tests for the linked list logic. Run with:  python -m unittest -v"""

import unittest

from task_list import TaskLinkedList


def tasks_of(linked_list):
    return [node.task for node in linked_list]


class TestTaskLinkedList(unittest.TestCase):
    def setUp(self):
        self.lst = TaskLinkedList()

    def test_empty(self):
        self.assertTrue(self.lst.is_empty())
        self.assertEqual(len(self.lst), 0)
        self.assertIsNone(self.lst.head)

    def test_add_first_and_last(self):
        self.lst.add_last("B")
        self.lst.add_first("A")
        self.lst.add_last("C")
        self.assertEqual(tasks_of(self.lst), ["A", "B", "C"])
        self.assertEqual(len(self.lst), 3)

    def test_pointers_are_linked(self):
        self.lst.add_last("A")
        self.lst.add_last("B")
        self.assertEqual(self.lst.head.next.task, "B")
        self.assertIsNone(self.lst.head.next.next)

    def test_insert_at(self):
        for t in "ABD":
            self.lst.add_last(t)
        self.lst.insert_at(2, "C")
        self.lst.insert_at(0, "0")
        self.lst.insert_at(5, "E")  # at the end
        self.assertEqual(tasks_of(self.lst), ["0", "A", "B", "C", "D", "E"])

    def test_insert_out_of_range(self):
        with self.assertRaises(IndexError):
            self.lst.insert_at(1, "X")
        with self.assertRaises(IndexError):
            self.lst.insert_at(-1, "X")

    def test_remove_at(self):
        for t in "ABCD":
            self.lst.add_last(t)
        self.assertEqual(self.lst.remove_at(0), "A")
        self.assertEqual(self.lst.remove_at(2), "D")
        self.assertEqual(self.lst.remove_at(0), "B")
        self.assertEqual(tasks_of(self.lst), ["C"])
        self.assertEqual(self.lst.remove_at(0), "C")
        self.assertTrue(self.lst.is_empty())

    def test_remove_out_of_range(self):
        with self.assertRaises(IndexError):
            self.lst.remove_at(0)

    def test_get_search_edit_toggle(self):
        for t in ("Buy milk", "Study Python", "Read book"):
            self.lst.add_last(t)
        self.assertEqual(self.lst.get(1).task, "Study Python")
        self.assertEqual(self.lst.search("PYTHON"), [1])
        self.assertEqual(self.lst.search("o"), [1, 2])
        self.assertEqual(self.lst.search("zzz"), [])
        self.lst.edit(0, "Buy bread")
        self.assertEqual(self.lst.get(0).task, "Buy bread")
        self.assertTrue(self.lst.toggle_completed(0))
        self.assertFalse(self.lst.toggle_completed(0))

    def test_reverse(self):
        for t in "ABCD":
            self.lst.add_last(t)
        self.lst.reverse()
        self.assertEqual(tasks_of(self.lst), ["D", "C", "B", "A"])
        self.assertEqual(len(self.lst), 4)
        self.lst.reverse()
        self.assertEqual(tasks_of(self.lst), ["A", "B", "C", "D"])

    def test_reverse_empty_and_single(self):
        self.lst.reverse()
        self.assertTrue(self.lst.is_empty())
        self.lst.add_last("A")
        self.lst.reverse()
        self.assertEqual(tasks_of(self.lst), ["A"])


if __name__ == "__main__":
    unittest.main()
