from test import OfficeTestCase
from movelister.format import FormatModifiedAction
from movelister.sheet import Overview
from movelister.model import ModifiedAction, Modifier


class FormatModifiedActionTestCase(OfficeTestCase):

    def setUp(self):
        super().setUp()
        self.overview = Overview('test sheet')
        self.overview.modifiers = [Modifier('aa'), Modifier('bb'), Modifier('cc')]
        self.modAct1 = ModifiedAction('attack 1', phases=2, hitPhase=1, default=True)
        self.modAct1.addModifier(0, Modifier('aa'))
        self.modAct1.addModifier(1, Modifier('bb'))
        self.overview.modifiedActions = [self.modAct1]

    def testFormatingModifiedAction(self):
        self.skipTest('modified action formatter not yet fully implemented')
        formatter = FormatModifiedAction(self.overview, self.modAct1)
        data = formatter.format()
        # name, hit, frames, phase, def, aa, bb, cc
        result = [
            ['attack 1', '', '', '0', 'x', 'x', '', ''],
            ['attack 1', 'x', '', '1', 'x', '', 'x', '']
        ]
        self.assertEqual(data, result)
