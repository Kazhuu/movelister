from test import OfficeTestCase
from movelister.format import ModifiedActionFormatter
from movelister.sheet import Overview
from movelister.model import ModifiedAction, Modifier


class ModifiedActionFormatterTestCase(OfficeTestCase):

    def setUp(self):
        super().setUp()
        self.overview = Overview('test sheet')
        self.overview.modifiers = [Modifier('aa'), Modifier('bb'), Modifier('cc')]
        self.modAct1 = ModifiedAction('attack 1', phases=2, hitPhase=1, default=True)
        self.modAct1.addModifier(0, Modifier('aa'))
        self.modAct1.addModifier(1, Modifier('bb'))
        self.overview.addModifiedAction(self.modAct1)

    def testFormatingModifiedAction(self):
        formatter = ModifiedActionFormatter(self.overview, self.modAct1, 3)
        data = formatter.format()
        # name, hit, frames, phase, def, aa, bb, cc, Notes1, Notes2, Notes3
        result = [
            ['attack 1', 'x', '', '0', 'x', 'x', '', '', '', '', ''],
            ['attack 1', '', '', '1', 'x', '', 'x', '', '', '', '']
        ]
        self.assertEqual(data, result)
