from test.officeTestCase import OfficeTestCase
from movelister.sheet.sheet import RESULT_LIST_SHEET_NAME
from movelister.sheet.results import Results
from movelister.core import styles


class ResultsTestCase(OfficeTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.results = Results(RESULT_LIST_SHEET_NAME)

    def testCreateResultStyles(self):
        styles.removeNonDefaultStyles()
        cellStyles = styles.getNonDefaultStyles()
        self.assertFalse(cellStyles)

        self.results.createResultStyles()
        cellStyles = styles.getNonDefaultStyles()
        self.assertIn('(Result)/Buffers', cellStyles)
