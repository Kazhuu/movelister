from test.officeTestCase import OfficeTestCase
from movelister.model.modifier import Modifier
from movelister.model.detail import Detail
from movelister.model.action import Action
from movelister.sheet.modifiers import Modifiers
from movelister.sheet.sheet import MODIFIER_LIST_SHEET_NAME


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
