from test import OfficeTestCase
from movelister import color
from movelister.sheet import Sheet


class ColorTestCase(OfficeTestCase):

    def testSettingCellBackColor(self):
        """
        Test setting cell back color with Color class value and then reading it
        back again. And then assert the values read back.
        """
        sheet = Sheet.getModifierSheetOld()
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
        Test reading cell default white cell color and check that Color.value
        returns the same value. Also assert individual colors too.

        TODO: Does't work yet. Fix the color class.
        """
        self.skipTest('Color.value not workin properly')
        sheet = Sheet.getAbout()
        cell = sheet.getCellByPosition(1, 1)
        c = color.Color(cell.CellBackColor)
        print(cell.CellBackColor)
        self.assertEqual(cell.CellBackColor, c.value)
        self.assertEqual(204, c.red)
        self.assertEqual(204, c.green)
        self.assertEqual(204, c.blue)
        self.assertEqual(204, c.alpha)
