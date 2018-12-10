from test import OfficeTestCase
from movelister.sheet import Master, MASTER_LIST_SHEET_NAME
from movelister.sheet.master import VIEW_COLUMN
from movelister.format import filter


class FilterTestCase(OfficeTestCase):

    def testFilterBy(self):
        master = Master(MASTER_LIST_SHEET_NAME)
        filteredRows = filter.filterRows(lambda row: row[VIEW_COLUMN] == 'Default', master.dataRows)
        self.assertTrue(filteredRows)
        for row in filteredRows:
            self.assertEqual(row[VIEW_COLUMN], 'Default')
