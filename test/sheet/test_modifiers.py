from test import OfficeTestCase
from movelister.sheet import Modifiers, MODIFIER_LIST_SHEET_NAME
from movelister.model import Modifier
from movelister.sheet.modifiers import COLOR_COLUMN, DATA_BEGIN_ROW


class ModifiersTestCase(OfficeTestCase):

    def testGetModifiers(self):
        modifier = Modifiers(MODIFIER_LIST_SHEET_NAME)
        modifiers = modifier.getModifiers()
        self.assertTrue(modifiers)
        for mod in modifiers:
            self.assertIsInstance(mod, Modifier)

    def testModifierColor(self):
        modifier = Modifiers(MODIFIER_LIST_SHEET_NAME)
        modifiers = modifier.getModifiers()
        firstActionColor = modifier.sheet.getCellByPosition(COLOR_COLUMN, DATA_BEGIN_ROW).CellBackColor
        self.assertEqual(modifiers[0].color, firstActionColor)
