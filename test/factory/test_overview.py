from test import OfficeTestCase
from movelister.factory import OverviewFactory
from movelister.sheet import Master
from movelister.sheet.sheet import MASTER_LIST_SHEET_NAME


class OverviewFactoryTestCase(OfficeTestCase):

    def testCreateOverview(self):
        master = Master(MASTER_LIST_SHEET_NAME)
        viewName = 'Default'
        overview = OverviewFactory.createOverview(master, viewName)
        modifiers = ['WPN1', 'WPN2', 'WPN3', 'Super', 'FL1', 'FL2', 'PG', 'LAM', 'PAM', 's b', 't b']
        modifiedActions = ['Attack s1', 'Attack s2', 'Attack s3', 'Attack s4', 'Swim', 'Rush']
        self.assertEqual(overview.name, viewName)
        self.assertTrue(all(modifier.name in modifiers for modifier in overview.modifiers))
        self.assertTrue(all(modAction.name in modifiedActions for modAction in overview.modifiedActions))
