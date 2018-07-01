from test.test_helper import OfficeTestCase
from movelister import color
from movelister.sheet import Sheet


class ColorTestCase(OfficeTestCase):

    def testSettingCellBackColor(self):
        sheet = Sheet.getModifierList()
        cell = sheet.getCellByPosition(0, 0)
        c = color.Color(0)
        c.alpha = 0
        c.red = 0
        c.green = 0
        c.blue = 255
        cell.CellBackColor = c.value
        # Read cell value again and assert that color changed.
        c2 = color.Color(sheet.getCellByPosition(0, 0).CellBackColor)
        self.assertEqual(c2.alpha, 0)
        self.assertEqual(c2.red, 0)
        self.assertEqual(c2.green, 0)
        self.assertEqual(c2.blue, 255)

    def testRead(self):
        sheet = Sheet.getModifierList()
        cell = sheet.getCellByPosition(0, 0)
        c = color.Color(0)
        c.alpha = 0
        c.red = 0
        c.green = 0
        c.blue = 255
        print(cell.CellBackColor)
