from test import OfficeTestCase
from movelister.format import generate
from movelister.sheet import Master, Overview, MASTER_LIST_SHEET_NAME


class GenerateTestCase(OfficeTestCase):

    def testGenerateOverview(self):
        master = Master(MASTER_LIST_SHEET_NAME)
        overview = Overview('Test overview')
        overview.setActions(master.getActions())
        generate.generateSheet(overview, 0)
