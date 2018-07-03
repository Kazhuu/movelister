from test.test_helper import OfficeTestCase

from movelister.sheet import Sheet


class SheetTestCase(OfficeTestCase):

    def testCreateNewSheet(self):
        """
        Test creating a new sheet with newSheet() method and then assert that
        it really happened.
        """
        Sheet.newSheet('test sheet', 0)
        sheet = Sheet.getByName('test sheet')
        self.assertEqual(sheet.getName(), 'test sheet')
