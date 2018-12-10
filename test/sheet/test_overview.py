from test import OfficeTestCase
from movelister.sheet import Overview, OVERVIEW_SHEET_NAME
from movelister.sheet.overview import MODIFIER_START_COLUM_NAME


class OverViewTestCase(OfficeTestCase):

    def testOverViewInstance(self):
        overview = Overview.fromSheet(OVERVIEW_SHEET_NAME)
        self.assertIsInstance(overview.data, list)
        self.assertTrue(overview.data)
        self.assertEqual(overview.name, OVERVIEW_SHEET_NAME)

    def testModifiersNames(self):
        overview = Overview.fromSheet(OVERVIEW_SHEET_NAME)
        modifiers = overview.modifiers
        self.assertTrue(modifiers)
        self.assertTrue(MODIFIER_START_COLUM_NAME not in modifiers)
        for modifier in modifiers:
            self.assertIsInstance(modifier, str)

    def testActionNames(self):
        overview = Overview.fromSheet(OVERVIEW_SHEET_NAME)
        actionNames = overview.actionNames
        self.assertTrue(actionNames)
        for action in actionNames:
            self.assertIsInstance(action, str)
