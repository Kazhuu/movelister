from test.officeTestCase import OfficeTestCase
from movelister.model.modifier import Modifier
from movelister.model.action import Action
from movelister.sheet.overview import Overview
from movelister.sheet.sheet import Sheet
from movelister.core import cursor, names
from movelister.format.overview import OverviewFormatter


class OverviewFormatterTestCase(OfficeTestCase):

    def setUp(self):
        super().setUp()
        self.sheetName = 'test'
        self.overview = Overview(self.sheetName)

    def testFormatHeader(self):
        self.overview.modifiers = [Modifier('aa'), Modifier('bb')]
        formatter = OverviewFormatter(self.overview)
        data = formatter.formatHeader()
        self.assertEqual(data, [
            'Action Name', 'Hit', 'Frames', 'Phase', 'DEF', 'aa', 'bb', 'Notes 1', 'Notes 2', 'Notes 3']
        )

    def testFormatModifiers(self):
        modifier1 = Modifier('aa')
        modifier2 = Modifier('bb')
        self.overview.modifiers = [modifier1, modifier2]

        modAct1 = Action('attack 1', phases=2, hitPhase=1, default=True)
        modAct1.addModifier(0, Modifier('aa'))
        modAct1.addModifier(1, Modifier('bb'))
        self.overview.addAction(modAct1)

        formatter = OverviewFormatter(self.overview)
        data = formatter.formatActions()
        self.assertEqual(data, [
            ['attack 1', 'x', '', '0', 'x', 'x', '', '', '', ''],
            ['attack 1', '', '', '1', 'x', '', 'x', '', '', '']]
        )

    def testFormat(self):
        modifier1 = Modifier('aa')
        modifier2 = Modifier('bb')
        modifier3 = Modifier('cc')
        self.overview.modifiers = [modifier1, modifier2, modifier3]

        modAct1 = Action('attack 1', phases=2, hitPhase=1, default=True)
        modAct1.addModifier(0, Modifier('aa'))
        modAct1.addModifier(1, Modifier('bb'))
        self.overview.addAction(modAct1)

        formatter = OverviewFormatter(self.overview)
        data = formatter.format()
        self.assertEqual(data, [
            ['', '', '', '', '', '', '', '', '', '', ''],
            ['Action Name', 'Hit', 'Frames', 'Phase', 'DEF', 'aa', 'bb', 'cc', 'Notes 1', 'Notes 2', 'Notes 3'],
            ['attack 1', 'x', '', '0', 'x', 'x', '', '', '', '', ''],
            ['attack 1', '', '', '1', 'x', '', 'x', '', '', '', '']]
        )

    def testGenerate(self):
        """
        Test generating new Overview-sheet from template, then assert that the
        sheet really exists and has generated content in it.
        """
        modifier1 = Modifier('aa')
        modifier2 = Modifier('bb')
        modifier3 = Modifier('cc')
        self.overview.modifiers = [modifier1, modifier2, modifier3]

        modAct1 = Action('attack 1', phases=2, hitPhase=1, default=True)
        modAct1.addModifier(0, Modifier('aa'))
        modAct1.addModifier(1, Modifier('bb'))
        self.overview.addAction(modAct1)

        formatter = OverviewFormatter(self.overview)
        formatter.generate()

        sheet = Sheet.getByName(names.getOverviewName(self.sheetName))
        data = cursor.getSheetContent(sheet)
        self.assertEqual(data, [
            ['', '', '', '', '', '', '', '', '', '', ''],
            ['Action Name', 'Hit', 'Frames', 'Phase', 'DEF', 'aa', 'bb', 'cc', 'Notes 1', 'Notes 2', 'Notes 3'],
            ['attack 1', 'x', '', '0', 'x', 'x', '', '', '', '', ''],
            ['attack 1', '', '', '1', 'x', '', 'x', '', '', '', '']]
        )
