import unittest
from project.algorithms.queue import Queue
from project.tests.test_utils import create_test_entity

class TestQueue(unittest.TestCase):
    def test_push_pop(self):
        q = Queue()
        e1 = create_test_entity("a", 0, 0)
        e2 = create_test_entity("b", 1, 1)
        q.push(e1)
        q.push(e2)
        self.assertEqual(q.first_motion(), e1)
        self.assertEqual(q.pop(), e1)
        self.assertEqual(q.first_motion(), e2)
        self.assertEqual(q.pop(), e2)
        self.assertTrue(q.is_empty())

    def test_restore_to_front(self):
        q = Queue()
        e1 = create_test_entity("a", 0, 0)
        e2 = create_test_entity("b", 1, 1)
        q.push(e1)
        q.push(e2)
        q.pop()
        q.restore_to_front(e1)
        self.assertEqual(q.first_motion(), e1)
        self.assertEqual(q.pop(), e1)
        self.assertEqual(q.pop(), e2)
