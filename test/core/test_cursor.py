from test import OfficeTestCase
from movelister.core import cursor
from movelister.sheet import Sheet


class CursorTestCase(OfficeTestCase):

    def testGetSheetContent(self):
        sheet = Sheet.getByName('Master List')
        data = cursor.getSheetContent(sheet)
        for row in data:
            self.assertIsInstance(row, list)
