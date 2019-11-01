from test import OfficeTestCase
from movelister.sheet import helper
from movelister.sheet import Master, MASTER_LIST_SHEET_NAME


class SheetHelperTestCase(OfficeTestCase):

    def setUp(self):
        self.master = Master(MASTER_LIST_SHEET_NAME)

    def testGetCellColorsFromColumn(self):
        colors = helper.getCellColorsFromColumn(self.master.sheet, self.master.colorColumnIndex,
                                                self.master.dataBeginRow, len(self.master.data))
        self.assertTrue(colors)
        for color in colors:
            self.assertIsInstance(color, int)
