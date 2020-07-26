from test.officeTestCase import OfficeTestCase

from movelister.core import namedRanges
from movelister.core.context import Context
from movelister.sheet.sheet import Sheet, MASTER_LIST_SHEET_NAME, MODIFIER_LIST_SHEET_NAME


class NamedRangesTestCase(OfficeTestCase):

    def testCreateNewNamedRange(self):
        """
        The test creates a new named range and then asserts it's there.
        """
        ranges = Context.getDocument().NamedRanges
        masterSheet = Sheet.getByName(MASTER_LIST_SHEET_NAME)

        namedRanges.createNewNamedRange(masterSheet, 'Test Name 1', ranges, 5, 20, 1, 3)
        namedRanges.createNewNamedRange(masterSheet, 'Test Name 2', ranges, 50, 70, 1, 3)

        self.assertTrue(ranges.hasByName('Test Name 1'))
        self.assertTrue(ranges.hasByName('Test Name 2'))

    def testDeleteFilteredNamedRanges(self):
        """
        The test creates named ranges in two sheets, then deletes the ranges from one of the sheets.
        It asserts if the correct ranges still exist.
        """
        ranges = Context.getDocument().NamedRanges
        masterSheet = Sheet.getByName(MASTER_LIST_SHEET_NAME)
        modifierSheet = Sheet.getByName(MODIFIER_LIST_SHEET_NAME)

        namedRanges.createNewNamedRange(masterSheet, 'Test Name 1', ranges, 15, 40, 1, 3)
        namedRanges.createNewNamedRange(masterSheet, 'Test Name 2', ranges, 60, 70, 1, 3)
        namedRanges.createNewNamedRange(modifierSheet, 'Test Name 3', ranges, 60, 70, 1, 3)

        namedRanges.deleteFilteredNamedRanges(ranges, MASTER_LIST_SHEET_NAME)

        self.assertFalse(ranges.hasByName('Test Name 1'))
        self.assertFalse(ranges.hasByName('Test Name 2'))
        self.assertTrue(ranges.hasByName('Test Name 3'))
