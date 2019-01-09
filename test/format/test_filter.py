from test import OfficeTestCase
from movelister.sheet import Master, MASTER_LIST_SHEET_NAME, Overview
from movelister.sheet.master import VIEW_COLUMN
from movelister.sheet.overview import NAME_COLUMN
from movelister.format import filter


class FilterTestCase(OfficeTestCase):

    def testFilterBy(self):
        master = Master(MASTER_LIST_SHEET_NAME)
        filteredRows = filter.filterRows(lambda row: row[VIEW_COLUMN] == 'Default', master.dataRows)
        self.assertTrue(filteredRows)
        for row in filteredRows:
            self.assertEqual(row[VIEW_COLUMN], 'Default')

    def testGroupRows(self):
        """
        Test that rows from overview are grouped together with same action name with
        """
        overview = Overview.fromSheet('Overview (default)')
        actionNames = overview.actionNames
        column = NAME_COLUMN
        groups = filter.groupRows(overview.dataRows, column)
        self.assertEqual(len(actionNames), len(groups))
        for group in groups:
            name = actionNames.pop(0)
            for row in group:
                self.assertEqual(name, row[column])
