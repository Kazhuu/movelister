from test import OfficeTestCase
from movelister.model import Modifier, Detail, Action
from movelister.sheet import Modifiers, MODIFIER_LIST_SHEET_NAME


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

    def testIsValidDetailSuccess(self):
        action = Action('action')
        modifiers = [Modifier('WPN1'), Modifier('WPN2')]
        detail = Detail(action, modifiers=modifiers)
        self.assertTrue(self.modifier.isValidDetail(detail))

    def testIsValidDetailNotSuccess(self):
        action = Action('action')
        modifiers = [Modifier('Fail')]
        detail = Detail(action, modifiers=modifiers)
        self.assertFalse(self.modifier.isValidDetail(detail))
