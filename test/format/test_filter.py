from test import OfficeTestCase
from movelister.sheet import Master
from movelister.sheet.master import VIEW_COLUMN
from movelister.format import filter


class FilterTestCase(OfficeTestCase):

    def testFilterBy(self):
        master = Master('Master List')
        filteredRows = filter.filterRows(lambda row: row[VIEW_COLUMN] == 'Default', master.dataRows)
        self.assertTrue(filteredRows)
        for row in filteredRows:
            self.assertEqual(row[VIEW_COLUMN], 'Default')
