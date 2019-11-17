from test import OfficeTestCase
from movelister.core import Alignment, cursor
from movelister.sheet import Master, MASTER_LIST_SHEET_NAME
from movelister.format import format


class FormatTestCase(OfficeTestCase):

    def testSettingAlignment(self):
        """
        A test that sets alignment to a range and then tests if it's what it should be.
        """
        self.skipTest('Test is unfinished because you have to compare the result to an uno Enum-object.')
        sheet = Master(MASTER_LIST_SHEET_NAME).sheet
        format.setHorizontalAlignmentToRange(sheet, Alignment.RIGHT, 1, 4)

        area = cursor.getSheetContent(sheet)
        cellRange = sheet.getCellRangeByPosition(1, 0, 1 + 4, len(area) - 1)
        self.assertEqual(cellRange.HoriJustify, 3)
