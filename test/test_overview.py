from test import OfficeTestCase
from movelister.sheet import Overview


class OverViewTestCase(OfficeTestCase):

    def testOverViewInstance(self):
        name = 'Overview (default)'
        overview = Overview(name)
        self.assertIsInstance(overview.data, tuple)
        self.assertEqual(name, overview.name)
