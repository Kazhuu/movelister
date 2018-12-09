from test import OfficeTestCase
from movelister.format import generate
from movelister.sheet import Master, Overview


class GenerateTestCase(OfficeTestCase):

    def testDrawOverview(self):
        master = Master('Master List')
        overview = Overview('Test overview')
        overview.setActions(master.getActions())
        generate.drawSheet(overview, 0)
