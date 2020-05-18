from test.officeTestCase import OfficeTestCase
from movelister.model.detail import Detail
from movelister.sheet.details import Details
from movelister.sheet.overview import Overview
from movelister.format.details import DetailsFormatter


class DetailsFormatterTestCase(OfficeTestCase):

    def setUp(self):
        super().setUp()
        self.sheetName = 'test'
        self.overview = Overview(self.sheetName)
        self.details = Details(self.sheetName)

    def testFormatHeader(self):
        """
        TODO: finish writing test.
        """
        pass

    def testDetailFormatting(self):
        """
        This test checks if Details formatting works as intended.
        TODO: doesn't seem to work yet. The result is just an empty array.
        """
        testDetail = Detail("Test Action", "Test Mod", [], {}, {})
        self.details.addDetail(testDetail)

        formatter = DetailsFormatter(self.details, self.overview)
        data = formatter.format()
        self.assertEqual(data, [['']])

    def testGenerate(self):
        """
        Test generating new Details-sheet from template, then assert that the
        sheet really exists and has generated content in it.
        TODO: finish writing test.
        """
        pass
