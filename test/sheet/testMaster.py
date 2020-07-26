from test.officeTestCase import OfficeTestCase
from movelister.sheet.master import Master
from movelister.sheet.sheet import MASTER_LIST_SHEET_NAME
from movelister.model.action import Action


class MasterTestCase(OfficeTestCase):

    def setUp(self):
        super().setUp()
        self.master = Master(MASTER_LIST_SHEET_NAME)
        self.actions = self.master.getActions()

    def testMasterInstance(self):
        self.assertIsInstance(self.master.data, list)
        self.assertEqual(self.master.name, MASTER_LIST_SHEET_NAME)
        self.assertEqual(len(self.master.actionColors), len(self.master.dataRows))

    def testGetActions(self):
        self.assertIsInstance(self.actions, list)
        self.assertTrue(self.actions)
        for action in self.actions:
            self.assertIsInstance(action, Action)

    def testGetActionsForView(self):
        actions = self.master.getActions('Target')
        self.assertTrue(actions[0].name, 'Minotaur (Idle)')

    def testGetDefaultActions(self):
        actions = self.master.getActions('Default')
        self.assertNotEqual(len(self.master.getActions()), len(actions))
