from test import OfficeTestCase
from movelister.sheet import Modifiers
from movelister.model import Modifier
from movelister.sheet.modifiers import COLOR_COLUMN, DATA_BEGIN_ROW


class ModifiersTestCase(OfficeTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.name = 'Modifier List'

    def testGetModifiers(self):
        modifier = Modifiers(self.name)
        modifiers = modifier.getModifiers()
        self.assertTrue(modifiers)
        for mod in modifiers:
            self.assertIsInstance(mod, Modifier)

    def testModifierColor(self):
        modifier = Modifiers(self.name)
        modifiers = modifier.getModifiers()
        firstActionColor = modifier.sheet.getCellByPosition(COLOR_COLUMN, DATA_BEGIN_ROW).CellBackColor
        self.assertEqual(modifiers[0].color, firstActionColor)
