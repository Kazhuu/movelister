import unittest

from test.officeTestCase import OfficeTestCase
from movelister.model.action import Action
from movelister.sheet.overview import Overview
from movelister.sheet.master import Master
from movelister.process.updateOverview import UpdateOverview
from movelister.process.factory import OverviewFactory
from movelister.sheet.sheet import MASTER_LIST_SHEET_NAME


class UpdateOverviewTestCase(OfficeTestCase):

    @unittest.skip('use old functionality, refactor')
    def testUpdate(self):
        """
        Split this test to smaller ones and test adding different things like modifiers
        and see they are updated corretly
        """
        overviewName = 'Default'
        oldOverviewName = 'Overview (Default)'
        newActionName = 'test attack'
        master = Master(MASTER_LIST_SHEET_NAME)
        newOverview = OverviewFactory.createOverview(master, overviewName)
        oldOverview = Overview.fromSheet(oldOverviewName)
        # Add new action to new overview. This should appear on updated
        # overview alongside with old actions and their data.
        oldOverview.addAction(Action(newActionName, phases=2, hitPhase=1, default=False))
        updatedOverview = UpdateOverview.update(oldOverview, newOverview)
        actions = updatedOverview.actions

        # Assert that new data includes added action in last index.
        self.assertEqual(actions[-1].name, newActionName)
        self.assertFalse(actions[-1].default)
        self.assertEqual(actions[-1].hitPhase, 1)
        # Assert hit phase is like in the old data.
        self.assertEqual(actions[0].hitPhase, 2)
        # Assert default is set like in the old data.
        self.assertTrue(actions[-2].default)
        self.assertFalse(actions[0].default)
        # Assert attack S1 action setted modifiers are like in the old data.
        # Assert phase 2 modifiers are like in the old data.
        attackS1Modifiers = actions[0].modifiers
        self.assertEqual(attackS1Modifiers[2][0].name, 'WPN1')
        self.assertEqual(attackS1Modifiers[2][1].name, 's b')
        self.assertEqual(attackS1Modifiers[2][2].name, 't b')
