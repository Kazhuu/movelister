from test.officeTestCase import OfficeTestCase
from movelister.core import cursor
from movelister.sheet.sheet import Sheet, MASTER_LIST_SHEET_NAME


class CursorTestCase(OfficeTestCase):

    def testGetSheetContent(self):
        masterSheet = Sheet.getByName(MASTER_LIST_SHEET_NAME)
        data = cursor.getSheetContent(masterSheet)
        for row in data:
            self.assertIsInstance(row, list)
