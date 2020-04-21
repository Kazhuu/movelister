from test.officeTestCase import OfficeTestCase
from movelister.sheet.sheet import MASTER_LIST_SHEET_NAME
from movelister.sheet.master import Master
from movelister.sheet.overview import Overview
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
        overview = Overview.fromSheet('Overview (default)')
        actionNames = overview.actionNames
        column = overview.nameColumnIndex
        groups = filter.groupRows(overview.dataRows, column)
        self.assertEqual(len(actionNames), len(groups))
        for group in groups:
            name = actionNames.pop(0)
            for row in group:
                self.assertEqual(name, row[column])
