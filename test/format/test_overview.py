from test import OfficeTestCase
from movelister.model import Modifier
from movelister.sheet import Overview


class OverviewFormatTestCase(OfficeTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sheetName = 'test overview'
        cls.overview = Overview(cls.sheetName)

    def testOverviewModifierFormat(self):
        # TODO: Finish test.
        self.overview.modifiers = [Modifier('aa'), Modifier('bb')]
