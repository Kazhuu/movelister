from test.test_helper import OfficeTestCase

from movelister.sheet import Sheet


class SheetTestCase(OfficeTestCase):

    def testCreateNewSheet(self):
        Sheet.newSheet('test sheet', 0)
        sheet = Sheet.getByName('test sheet')
        self.assertEqual(sheet.getName(), 'test sheet')
