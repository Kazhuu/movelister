from test.officeTestCase import OfficeTestCase
from movelister.core.context import Context
from movelister.sheet import helper
from movelister.sheet.master import Master
from movelister.sheet.sheet import MASTER_LIST_SHEET_NAME


class SheetHelperTestCase(OfficeTestCase):

    def setUp(self):
        super().setUp()
        self.master = Master(MASTER_LIST_SHEET_NAME)

    def testGetActiveSheetName(self):
        """
        This test checks if active Sheet name is successfully acquired by this Helper-function.
        """
        document = Context.getDocument()
        # activeSheet = document.getCurrentController().getActiveSheet()
        # activeSheet.setName('testname')
        # name = helper.getActiveSheetName()
        # self.assertEqual(name, 'testname')

    def testGetCellColorsFromColumn(self):
        """
        This test checks if this function actually gets colors from the Sheet.
        """
        colors = helper.getCellColorsFromColumn(self.master.sheet, self.master.colorColumnIndex,
                                                self.master.dataBeginRow, len(self.master.data))
        self.assertTrue(colors)
        for color in colors:
            self.assertIsInstance(color, int)

    def testGetColumnPosition(self):
        """
        This test checks if the Helper-function GetColumnPosition does what is advertised.
        """
        number = helper.getColumnPosition(self.master.data, 'Color')
        self.assertEqual(number, 3)
