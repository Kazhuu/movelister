from test import OfficeTestCase
from movelister.model import Modifier, ModifiedAction
from movelister.sheet import Overview, Sheet
from movelister.core import cursor
from movelister.format import OverviewFormatter


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

        modAct1 = ModifiedAction('attack 1', phases=2, hitPhase=1, default=True)
        modAct1.addModifier(0, Modifier('aa'))
        modAct1.addModifier(1, Modifier('bb'))
        self.overview.addModifiedAction(modAct1)

        formatter = OverviewFormatter(self.overview)
        data = formatter.formatModifiedActions()
        self.assertEqual(data, [
            ['attack 1', 'x', '', '0', 'x', 'x', '', '', '', ''],
            ['attack 1', '', '', '1', 'x', '', 'x', '', '', '']]
        )

    def testFormat(self):
        modifier1 = Modifier('aa')
        modifier2 = Modifier('bb')
        modifier3 = Modifier('cc')
        self.overview.modifiers = [modifier1, modifier2, modifier3]

        modAct1 = ModifiedAction('attack 1', phases=2, hitPhase=1, default=True)
        modAct1.addModifier(0, Modifier('aa'))
        modAct1.addModifier(1, Modifier('bb'))
        self.overview.addModifiedAction(modAct1)

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
        Test generating new overview sheet from template and after that assert that
        sheet really exists and has generated content in it.
        """
        modifier1 = Modifier('aa')
        modifier2 = Modifier('bb')
        modifier3 = Modifier('cc')
        self.overview.modifiers = [modifier1, modifier2, modifier3]

        modAct1 = ModifiedAction('attack 1', phases=2, hitPhase=1, default=True)
        modAct1.addModifier(0, Modifier('aa'))
        modAct1.addModifier(1, Modifier('bb'))
        self.overview.addModifiedAction(modAct1)

        formatter = OverviewFormatter(self.overview)
        formatter.generate()

        sheet = Sheet.getByName('Overview ({0})'.format(self.sheetName))
        data = cursor.getSheetContent(sheet)
        self.assertEqual(data, [
            ['', '', '', '', '', '', '', '', '', '', ''],
            ['Action Name', 'Hit', 'Frames', 'Phase', 'DEF', 'aa', 'bb', 'cc', 'Notes 1', 'Notes 2', 'Notes 3'],
            ['attack 1', 'x', '', '0', 'x', 'x', '', '', '', '', ''],
            ['attack 1', '', '', '1', 'x', '', 'x', '', '', '', '']]
        )
