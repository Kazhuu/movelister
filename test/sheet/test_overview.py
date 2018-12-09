from test import OfficeTestCase
from movelister.sheet import Overview


class OverViewTestCase(OfficeTestCase):

    def testOverViewInstance(self):
        name = 'Overview (default)'
        overview = Overview.fromSheet(name)
        self.assertIsInstance(overview.data, tuple)
        self.assertTrue(overview.data)
        print(overview.data)
        self.assertEqual(name, overview.name)
