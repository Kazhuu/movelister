from test import OfficeTestCase
from movelister.core import Context
from movelister.sheet import Sheet


class SheetTestCase(OfficeTestCase):

    def testCreateNewSheet(self):
        Sheet.newSheet('test sheet', 0)
        sheet = Sheet.getByName('test sheet')
        self.assertEqual(sheet.getName(), 'test sheet')

    def testGetPosition(self):
        position = Sheet.getPosition('Modifier List')
        self.assertEqual(position, 4)

    def testGetWrongPosition(self):
        with self.assertRaises(ValueError):
            Sheet.getPosition('fails')

    def testGetSheetNames(self):
        names = Sheet.getSheetNames()
        for name in names:
            self.assertIsInstance(name, str)

    def testNewSheetRightOf(self):
        rightOfName = 'Master List'
        name = 'test sheet'
        sheet = Sheet.newSheetRightOf(rightOfName, name)
        self.assertEqual(name, sheet.getName())
        names = Context.getDocument().Sheets.getElementNames()
        index = names.index(rightOfName)
        self.assertEqual(index + 1, names.index(name))

    def testNewSheetLeftOf(self):
        leftOfName = 'Modifier List'
        name = 'test sheet'
        sheet = Sheet.newSheetLeftOf(leftOfName, name)
        self.assertEqual(name, sheet.getName())
        names = Context.getDocument().Sheets.getElementNames()
        index = names.index(leftOfName)
        self.assertEqual(index - 1, names.index(name))

    def testNewSheetRightOfWithWrongName(self):
        rightOfName = 'fail'
        with self.assertRaises(ValueError):
            Sheet.newSheetRightOf(rightOfName, 'will fail')
