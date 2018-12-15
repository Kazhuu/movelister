from test import OfficeTestCase
from movelister.sheet import helper
from movelister.sheet import Master, MASTER_LIST_SHEET_NAME
from movelister.sheet.master import COLOR_COLUMN, DATA_BEGIN_ROW


class SheetHelperTestCase(OfficeTestCase):

    def setUp(self):
        self.master = Master(MASTER_LIST_SHEET_NAME)

    def testGetCellColorsFromColumn(self):
        colors = helper.getCellColorsFromColumn(self.master.sheet, COLOR_COLUMN, DATA_BEGIN_ROW, len(self.master.data))
        self.assertTrue(colors)
        for color in colors:
            self.assertIsInstance(color, int)
