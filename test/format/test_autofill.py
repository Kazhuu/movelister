from test import OfficeTestCase
from movelister.sheet import Master, MASTER_LIST_SHEET_NAME
from movelister.sheet.master import VIEW_COLUMN, INPUTS_COLUMN, PHASE_COLUMN
from movelister.format import autofill


class AutoFillTestCase(OfficeTestCase):

    def testAutoFillMasterList(self):
        master = Master(MASTER_LIST_SHEET_NAME)

        # change some values to empty in the Master List.
        master.sheet.getCellByPosition(VIEW_COLUMN, 3).setString('')
        master.sheet.getCellByPosition(INPUTS_COLUMN, 3).setString('')
        master.sheet.getCellByPosition(PHASE_COLUMN, 3).setString('')

        # autofill Master List.
        autofill.autoFillMasterList(master)

        # read Master List again and assert values are like they should.
        self.assertEqual(master.sheet.getCellByPosition(VIEW_COLUMN, 3).getString(), 'Default')
        self.assertEqual(master.sheet.getCellByPosition(INPUTS_COLUMN, 3).getString(), 'Default')
        self.assertEqual(master.sheet.getCellByPosition(PHASE_COLUMN, 3).getString(), '0')
