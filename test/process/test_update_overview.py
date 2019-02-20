from test import OfficeTestCase
from movelister.model import ModifiedAction
from movelister.sheet import Overview, Master
from movelister.process import UpdateOverview, OverviewFactory
from movelister.sheet.sheet import MASTER_LIST_SHEET_NAME


class UpdateOverviewTestCase(OfficeTestCase):

    def testUpdate(self):
        overviewName = 'Default'
        oldOverviewName = 'Overview (Default)'
        newActionName = 'test attack'
        master = Master(MASTER_LIST_SHEET_NAME)
        newOverview = OverviewFactory.createOverview(master, overviewName)
        oldOverview = Overview.fromSheet(oldOverviewName)
        # Add new action to new overview. This should appear on updated
        # overview alongside with old actions and their data.
        newOverview.addModifiedAction(ModifiedAction(newActionName, phases=2, hitPhase=1, default=False))
        updatedOverview = UpdateOverview.update(oldOverview, newOverview)
        modActions = updatedOverview.modifiedActions

        # Assert that new data includes added modified action in last index.
        self.assertEqual(modActions[-1].name, newActionName)
        self.assertFalse(modActions[-1].default)
        self.assertEqual(modActions[-1].hitPhase, 1)
        # Assert hit phase is like in the old data.
        self.assertEqual(modActions[0].hitPhase, 2)
        # Assert default is set like in the old data.
        self.assertTrue(modActions[-2].default)
        self.assertFalse(modActions[0].default)
        # Assert attack S1 modified action setted modifiers are like in the old data.
        # Assert phase 2 modifiers are like in the old data.
        attackS1Modifiers = modActions[0].modifiers
        self.assertEqual(attackS1Modifiers[2][0].name, 'WPN1')
        self.assertEqual(attackS1Modifiers[2][1].name, 's b')
        self.assertEqual(attackS1Modifiers[2][2].name, 't b')
