from test import OfficeTestCase
from movelister.sheet import Master
from movelister.model import Action
from movelister.sheet.master import COLOR_COLUMN, DATA_BEGIN_ROW


class MasterTestCase(OfficeTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.name = 'Master List'

    def testMasterInstance(self):
        master = Master(self.name)
        self.assertIsInstance(master.data, tuple)
        self.assertEqual(self.name, master.name)
        self.assertEqual(len(master.actionColors), len(master.dataRows))

    def testGetActions(self):
        master = Master(self.name)
        actions = master.getActions()
        self.assertIsInstance(actions, list)
        self.assertTrue(actions)
        for action in actions:
            self.assertIsInstance(action, Action)

    def testGetDefaultActions(self):
        master = Master(self.name)
        actions = master.getActions('Default')
        self.assertNotEqual(len(master.getActions()), len(actions))

    def testActionColor(self):
        master = Master(self.name)
        actions = master.getActions()
        firstActionColor = master.sheet.getCellByPosition(COLOR_COLUMN, DATA_BEGIN_ROW).CellBackColor
        self.assertEqual(firstActionColor, actions[0].color)
