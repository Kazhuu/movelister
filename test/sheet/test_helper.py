from test import OfficeTestCase
from movelister.sheet import helper
from movelister.sheet import Master, MASTER_LIST_SHEET_NAME
from movelister.sheet.master import COLOR_COLUMN, DATA_BEGIN_ROW


class SheetHelperTestCase(OfficeTestCase):

    def testGetCellColorsFromColumn(self):
        masterSheet = Master(MASTER_LIST_SHEET_NAME)
        colors = helper.getCellColorsFromColumn(masterSheet.sheet, COLOR_COLUMN, DATA_BEGIN_ROW, len(masterSheet.data))
        self.assertTrue(colors)
        for color in colors:
            self.assertIsInstance(color, int)
