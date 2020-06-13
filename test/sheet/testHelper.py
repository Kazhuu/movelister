from test.officeTestCase import OfficeTestCase
from movelister.core.context import Context
from movelister.sheet import helper
from movelister.sheet.master import Master
from movelister.sheet.sheet import MASTER_LIST_SHEET_NAME


class SheetHelperTestCase(OfficeTestCase):

    def setUp(self):
        super().setUp()
        self.master = Master(MASTER_LIST_SHEET_NAME)

    def testCreateEmptyRow(self):
        """
        This test checks if this function adds an empty row.
        """
        data = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
        data.append(helper.createEmptyRow(3))
        self.assertEqual(data, [[1, 2, 3], [1, 2, 3], [1, 2, 3], ['', '', '']])

    def testGetActiveSheetName(self):
        """
        This test checks if active Sheet name is successfully acquired by this Helper-function.
        Note: this test requires that the template sheet opens with Master List active.
        """
        document = Context.getDocument()
        activeSheet = document.getCurrentController().getActiveSheet()
        name = helper.getActiveSheetName()
        self.assertEqual(name, 'Master List')

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

    def testNormalizeArray(self):
        """
        This test checks if the Helper-function Normalize Array does what is advertised.
        """
        data = [[1, 2, 3], [1, 2, 3], [1, 2, 3, 4]]
        helper.normalizeArray(data)
        self.assertEqual(data, [[1, 2, 3, ''], [1, 2, 3, ''], [1, 2, 3, 4]])
