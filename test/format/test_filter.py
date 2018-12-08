from test import OfficeTestCase
from movelister.sheet import Master
from movelister.sheet import master
from movelister.format import filter


class FilterTestCase(OfficeTestCase):

    def testFilterBy(self):
        masterSheet = Master('Master List')
        filteredRows = filter.filterRows(lambda row: row[master.VIEW_COLUMN] == 'Default', masterSheet.dataRows)
        self.assertTrue(filteredRows)
        for row in filteredRows:
            self.assertEqual(row[master.VIEW_COLUMN], 'Default')
