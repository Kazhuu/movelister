from test import OfficeTestCase
from movelister.sheet import Master
from movelister.action import Action


class MasterTestCase(OfficeTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.name = 'Master List'

    def testMasterInstance(self):
        master = Master(self.name)
        self.assertIsInstance(master.data, tuple)
        self.assertEqual(self.name, master.name)

    def testGetActions(self):
        master = Master(self.name)
        actions = master.getActions()
        self.assertIsInstance(actions, list)
        for action in actions:
            self.assertIsInstance(action, Action)
