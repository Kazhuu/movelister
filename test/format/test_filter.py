from test import OfficeTestCase
from movelister.sheet import Master, MASTER_LIST_SHEET_NAME, Overview, OVERVIEW_SHEET_NAME
from movelister.format import filter


class FilterTestCase(OfficeTestCase):

    def testFilterBy(self):
        master = Master(MASTER_LIST_SHEET_NAME)
        filteredRows = filter.filterRows(lambda row: row[master.viewColumnIndex] == 'Default', master.dataRows)
        self.assertTrue(filteredRows)
        for row in filteredRows:
            self.assertEqual(row[master.viewColumnIndex], 'Default')

    def testGroupRows(self):
        """
        Test that rows from overview are grouped together with same action name with
        """
        overview = Overview.fromSheet(OVERVIEW_SHEET_NAME)
        actionNames = overview.actionNames
        column = overview.nameColumnIndex
        groups = filter.groupRows(overview.dataRows, column)
        self.assertEqual(len(actionNames), len(groups))
        for group in groups:
            name = actionNames.pop(0)
            for row in group:
                self.assertEqual(name, row[column])
