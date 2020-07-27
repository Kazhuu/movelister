from test.officeTestCase import OfficeTestCase
from movelister.core import namedRanges
from movelister.sheet.sheet import Sheet


class NamedRangesTestCase(OfficeTestCase):

    def setUp(self):
        super().setUp()
        self.detailsUnoSheet = Sheet.getByName('Details (Default)')

    def testCreateNewNamedRange(self):
        self.assertFalse(namedRanges.getNameRanges())

        ranges = namedRanges.NamedRanges(self.detailsUnoSheet, 0, 'Default')
        ranges.generate()
        rangesList = namedRanges.getNameRanges()

        self.assertIn('Attack s1 (Default)', rangesList)
