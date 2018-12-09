from test import OfficeTestCase
from movelister.sheet import draw, Master, Overview


class GenerateTestCase(OfficeTestCase):

    def testDrawOverview(self):
        master = Master('Master List')
        overview = Overview('Test overview')
        overview.setActions(master.getActions())
        draw.drawSheet(overview, 0)
