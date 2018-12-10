from test import OfficeTestCase
from movelister.sheet import Master, MASTER_LIST_SHEET_NAME
from movelister.model import Action
from movelister.sheet.master import COLOR_COLUMN, DATA_BEGIN_ROW


class MasterTestCase(OfficeTestCase):

    def testMasterInstance(self):
        master = Master(MASTER_LIST_SHEET_NAME)
        self.assertIsInstance(master.data, list)
        self.assertEqual(master.name, MASTER_LIST_SHEET_NAME)
        self.assertEqual(len(master.actionColors), len(master.dataRows))

    def testGetActions(self):
        master = Master(MASTER_LIST_SHEET_NAME)
        actions = master.getActions()
        self.assertIsInstance(actions, list)
        self.assertTrue(actions)
        for action in actions:
            self.assertIsInstance(action, Action)

    def testGetDefaultActions(self):
        master = Master(MASTER_LIST_SHEET_NAME)
        actions = master.getActions('Default')
        self.assertNotEqual(len(master.getActions()), len(actions))

    def testActionColor(self):
        master = Master(MASTER_LIST_SHEET_NAME)
        actions = master.getActions()
        firstActionColor = master.sheet.getCellByPosition(COLOR_COLUMN, DATA_BEGIN_ROW).CellBackColor
        self.assertEqual(actions[0].color, firstActionColor)
