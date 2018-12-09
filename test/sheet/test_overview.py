from test import OfficeTestCase
from movelister.sheet import Overview


class OverViewTestCase(OfficeTestCase):

    def testOverViewInstance(self):
        name = 'Overview (Default)'
        overview = Overview.fromSheet(name)
        self.assertIsInstance(overview.data, list)
        self.assertTrue(overview.data)
        self.assertEqual(overview.name, name)
