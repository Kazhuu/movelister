from test import OfficeTestCase
from movelister.sheet import Master
from movelister.format import filter


class FilterTestCase(OfficeTestCase):

    def testFilterBy(self):
        def defaultFilter(row):
            return row[0] == 'Default'
        master = Master('Master List')
        filteredRows = filter.filterRows(master.data, defaultFilter)
        self.assertTrue(filteredRows)
        for row in filteredRows:
            self.assertEqual(row[0], 'Default')
