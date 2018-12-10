from test import OfficeTestCase
from movelister.sheet import Overview, OVERVIEW_SHEET_NAME


class OverViewTestCase(OfficeTestCase):

    def testOverViewInstance(self):
        overview = Overview.fromSheet(OVERVIEW_SHEET_NAME)
        self.assertIsInstance(overview.data, list)
        self.assertTrue(overview.data)
        self.assertEqual(overview.name, OVERVIEW_SHEET_NAME)
