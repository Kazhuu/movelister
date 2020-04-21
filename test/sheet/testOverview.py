from test.officeTestCase import OfficeTestCase
from movelister.model.action import Action
from movelister.model.modifier import Modifier
from movelister.sheet.overview import Overview


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

    def testAddAction(self):
        action1 = Action('action1')
        action2 = Action('action2')
        overview = Overview('test')
        overview.addAction(action1)
        overview.addAction(action2)
        self.assertEqual(overview.actions, [action1, action2])

    def testFindAction(self):
        action1 = Action('action1')
        action2 = Action('action2')
        action3 = Action('action3')
        overview = Overview('test')
        overview.addAction(action1)
        overview.addAction(action2)
        overview.addAction(action3)
        self.assertTrue(action2.name == overview.findAction(action2).name)
        self.assertIsNone(overview.findAction(Action('cannot find')))

    def testActionNames(self):
        actionNames = self.overview.actionNames
        self.assertTrue(actionNames)
        for action in actionNames:
            self.assertIsInstance(action, str)

    def testGetActions(self):
        actions = self.overview.actions
        self.assertTrue(actions)
        for action in actions:
            self.assertIsInstance(action, Action)

    def testActionModifiers(self):
        """
        Test Action modifiers for phase 2 that data is formed according
        to data set in the Overview sheet.
        """
        names = ['WPN1', 's b', 't b']
        actions = self.overview.actions
        modifiers = actions[0].getModifiersByPhase(2)
        self.assertTrue(all(modifier.name in names for modifier in modifiers))
