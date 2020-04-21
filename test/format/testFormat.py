from com.sun.star.table.CellHoriJustify import RIGHT

from test.officeTestCase import OfficeTestCase
from movelister.core import cursor
from movelister.core.alignment import HorizontalAlignment, VerticalAlignment
from movelister.sheet import Master, MASTER_LIST_SHEET_NAME
from movelister.format import format


class FormatTestCase(OfficeTestCase):

    def testSetHorizontalAlignmentToRange(self):
        """
        A test that sets horizontal alignment to a range and then tests if it's what it should be.
        """
        sheet = Master(MASTER_LIST_SHEET_NAME).sheet
        format.setHorizontalAlignmentToRange(sheet, HorizontalAlignment.RIGHT, 1, 4)

        area = cursor.getSheetContent(sheet)
        cellRange = sheet.getCellRangeByPosition(1, 0, 1 + 4, len(area) - 1)
        self.assertEqual(cellRange.HoriJustify, CellHoriJustify.RIGHT)

    def testSetVerticalAlignmentToRange(self):
        """
        A test that sets vertical alignment to a range and then tests if it's what it should be.
        """
        sheet = Master(MASTER_LIST_SHEET_NAME).sheet
        format.setVerticalAlignmentToRange(sheet, VerticalAlignment.CENTER, 1, 10, 20, 25)

        cellRange = sheet.getCellRangeByPosition(1, 10, 20, 25)
        self.assertEqual(cellRange.VertJustify, 2)
