from test import OfficeTestCase
from movelister.model import Modifier
from movelister.sheet import Overview
from movelister.format import FormatOverview


class OverviewFormatTestCase(OfficeTestCase):

    def setUp(self):
        super().setUp()
        self.sheetName = 'test overview'
        self.overview = Overview(self.sheetName)

    def testOverviewFormatHeader(self):
        self.overview.modifiers = [Modifier('aa'), Modifier('bb')]
        format = FormatOverview(self.overview)
        data = format.format()
        self.assertEqual(data, [
            ['Action Name', 'Hit', 'Frames', 'Phase',
             'DEF', 'aa', 'bb', 'Notes 1', 'Notes 2', 'Notes 3']]
        )
