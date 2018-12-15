from test import OfficeTestCase
from movelister.sheet import Modifiers, MODIFIER_LIST_SHEET_NAME
from movelister.model import Modifier
from movelister.sheet.modifiers import COLOR_COLUMN, DATA_BEGIN_ROW


class ModifiersTestCase(OfficeTestCase):

    def setUp(self):
        self.modifier = Modifiers(MODIFIER_LIST_SHEET_NAME)
        self.modifiers = self.modifier.getModifiers()

    def testGetModifiers(self):
        self.assertTrue(self.modifiers)
        for mod in self.modifiers:
            self.assertIsInstance(mod, Modifier)

    def testModifierColor(self):
        firstActionColor = self.modifier.sheet.getCellByPosition(COLOR_COLUMN, DATA_BEGIN_ROW).CellBackColor
        self.assertEqual(self.modifiers[0].color, firstActionColor)
