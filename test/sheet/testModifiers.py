from test import OfficeTestCase
from movelister.sheet import Modifiers, MODIFIER_LIST_SHEET_NAME
from movelister.model import Modifier


class ModifiersTestCase(OfficeTestCase):

    def setUp(self):
        self.modifier = Modifiers(MODIFIER_LIST_SHEET_NAME)
        self.modifiers = self.modifier.getModifiers()

    def testGetModifiers(self):
        self.assertTrue(self.modifiers)
        for mod in self.modifiers:
            self.assertIsInstance(mod, Modifier)

    def testModifierColor(self):
        firstActionColor = self.modifier.sheet.getCellByPosition(self.modifier.colorColumnIndex,
                                                                 self.modifier.dataBeginRow).CellBackColor
        self.assertEqual(self.modifiers[0].color, firstActionColor)
