from test import OfficeTestCase
from movelister.format import ActionFormatter
from movelister.sheet import Overview
from movelister.model import Action, Modifier


class ActionFormatterTestCase(OfficeTestCase):

    def setUp(self):
        super().setUp()
        self.overview = Overview('test sheet')
        self.overview.modifiers = [Modifier('aa'), Modifier('bb'), Modifier('cc')]
        self.action = Action('attack 1', phases=2, hitPhase=1, default=True)
        self.action.addModifier(0, Modifier('aa'))
        self.action.addModifier(1, Modifier('bb'))
        self.overview.addAction(self.action)
        # TODO: this test doesn't take all things in Action class into account, like notes.

    def testFormattingAction(self):
        formatter = ActionFormatter(self.overview, self.action, 3)
        data = formatter.format()
        # name, hit, frames, phase, def, aa, bb, cc
        result = [
            ['attack 1', 'x', '', '0', 'x', 'x', '', ''],
            ['attack 1', '', '', '1', 'x', '', 'x', '']
        ]
        self.assertEqual(data, result)
