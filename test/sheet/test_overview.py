from test import OfficeTestCase
from movelister.model import ModifiedAction
from movelister.sheet import Overview, OVERVIEW_SHEET_NAME


class OverviewTestCase(OfficeTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.overview = Overview.fromSheet(OVERVIEW_SHEET_NAME)

    def testOverviewInstance(self):
        self.assertIsInstance(self.overview.data, list)
        self.assertTrue(self.overview.data)
        self.assertEqual(self.overview.name, OVERVIEW_SHEET_NAME)

    def testModifiers(self):
        names = ['WPN1', 'WPN2', 'WPN3', 'Super', 'FL1', 'FL2', 'PG', 'LAM', 'PAM', 's b', 't b']
        modifiers = self.overview.modifiers
        self.assertTrue(all(modifier.name in names for modifier in modifiers))

    def testActionNames(self):
        actionNames = self.overview.actionNames
        self.assertTrue(actionNames)
        for action in actionNames:
            self.assertIsInstance(action, str)

    def testGetModifiedActions(self):
        modifiedActions = self.overview.modifiedActions
        self.assertTrue(modifiedActions)
        for modifiedAction in modifiedActions:
            self.assertIsInstance(modifiedAction, ModifiedAction)

    def testModifiedActionModifiers(self):
        """
        Test ModifiedAction modifiers for phase 2 that data is formed according
        to data set in the overview sheet.
        """
        names = ['WPN1', 's b', 't b']
        modifiedActions = self.overview.modifiedActions
        modifiers = modifiedActions[0].phaseModifiers(2)
        self.assertTrue(all(modifier.name in names for modifier in modifiers))
