from test import OfficeTestCase
from movelister.sheet import Master, MASTER_LIST_SHEET_NAME
from movelister.model import Action, ModifiedAction


class MasterTestCase(OfficeTestCase):

    def setUp(self):
        self.master = Master(MASTER_LIST_SHEET_NAME)
        self.actions = self.master.getActions()
        self.modifiedActions = self.master.getModifiedActions()

    def testMasterInstance(self):
        self.assertIsInstance(self.master.data, list)
        self.assertEqual(self.master.name, MASTER_LIST_SHEET_NAME)
        self.assertEqual(len(self.master.actionColors), len(self.master.dataRows))

    def testGetActions(self):
        self.assertIsInstance(self.actions, list)
        self.assertTrue(self.actions)
        for action in self.actions:
            self.assertIsInstance(action, Action)

    def testGetModifiedActions(self):
        self.assertIsInstance(self.modifiedActions, list)
        self.assertTrue(self.modifiedActions)
        for modifiedAction in self.modifiedActions:
            self.assertIsInstance(modifiedAction, ModifiedAction)

    def testGetDefaultActions(self):
        actions = self.master.getActions('Default')
        self.assertNotEqual(len(self.master.getActions()), len(actions))

    def testActionColor(self):
        firstActionColor = self.master.sheet.getCellByPosition(self.master.colorColumnIndex,
                                                               self.master.dataBeginRow).CellBackColor
        self.assertEqual(self.actions[0].color, firstActionColor)
