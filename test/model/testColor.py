from test.officeTestCase import OfficeTestCase
from movelister.model import color
from movelister.sheet.modifiers import Modifiers


class ColorTestCase(OfficeTestCase):

    def testSettingCellBackColor(self):
        """
        Test setting CellBackColor with values from Color class and then reading it
        back again. And then assert the values read back.

        Note: this test will fail on Windows because test opens Document in read-only.
        """
        sheet = Modifiers('Modifiers').sheet
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
        """
        Test reading color value from a cell and check that Color.value
        returns the same value. Also asserts individual colors.
        """
        sheet = Modifiers('Modifiers').sheet
        cell = sheet.getCellByPosition(0, 0)
        c = color.Color(cell.CellBackColor)
        self.assertEqual(c.value, cell.CellBackColor)
        self.assertEqual(c.red, 230)
        self.assertEqual(c.green, 230)
        self.assertEqual(c.blue, 255)
        self.assertEqual(c.alpha, 0)
