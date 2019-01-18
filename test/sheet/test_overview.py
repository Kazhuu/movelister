from test import OfficeTestCase
from movelister.model import ModifiedAction, Modifier
from movelister.sheet import Overview


class OverviewTestCase(OfficeTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.overviewName = 'Overview (default)'
        cls.overview = Overview.fromSheet(cls.overviewName)

    def testOverviewInstance(self):
        self.assertIsInstance(self.overview.data, list)
        self.assertTrue(self.overview.data)
        self.assertEqual(self.overview.name, self.overviewName)

    def testModifiers(self):
        names = ['WPN1', 'WPN2', 'WPN3', 'Super', 'FL1', 'FL2', 'PG', 'LAM', 'PAM', 's b', 't b']
        modifiers = self.overview.modifiers
        self.assertTrue(all(modifier.name in names for modifier in modifiers))

    def testAddModifier(self):
        modifier1 = Modifier('mods1')
        modifier2 = Modifier('mods2')
        overview = Overview('test')
        overview.addModifier(modifier1)
        overview.addModifier(modifier2)
        self.assertEqual(overview.modifiers, [modifier1, modifier2])

    def testAddModifiedAction(self):
        modifiedAction1 = ModifiedAction('modAction1')
        modifiedAction2 = ModifiedAction('modAction2')
        overview = Overview('test')
        overview.addModifiedAction(modifiedAction1)
        overview.addModifiedAction(modifiedAction2)
        self.assertEqual(overview.modifiedActions, [modifiedAction1, modifiedAction2])

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
