from test import OfficeTestCase
from movelister.sheet import helper
from movelister.sheet import Master
from movelister.sheet.master import COLOR_COLUMN, DATA_BEGIN_ROW


class SheetHelperTestCase(OfficeTestCase):

    def testGetCellColorsFromColumn(self):
        masterSheet = Master('Master List')
        colors = helper.getCellColorsFromColumn(masterSheet.sheet, COLOR_COLUMN, DATA_BEGIN_ROW, len(masterSheet.data))
        self.assertTrue(colors)
        for color in colors:
            self.assertIsInstance(color, int)
