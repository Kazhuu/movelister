import unittest
from movelister.model.action import Action


class ActionTestCase(unittest.TestCase):

    def setUp(self):
        self.action1 = Action('aaa')
        self.action2 = Action('aaa')
        self.action3 = Action('bbb')

    def testEquality(self):
        self.assertTrue(self.action1 == self.action2)
        self.assertFalse(self.action1 == self.action3)

    def testNonequality(self):
        self.assertTrue(self.action1 != self.action3)
        self.assertFalse(self.action1 != self.action2)
