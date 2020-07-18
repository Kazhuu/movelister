from test.officeTestCase import OfficeTestCase
from movelister.format.action import ActionFormatter
from movelister.sheet.overview import Overview
from movelister.model.action import Action
from movelister.model.modifier import Modifier


class ActionFormatterTestCase(OfficeTestCase):

    def setUp(self):
        super().setUp()
        self.overview = Overview('test sheet')
        self.overview.modifiers = [Modifier('aa'), Modifier('bb'), Modifier('cc')]
        self.action = Action('attack 1', phases=2, hitPhase=1, default=True)
        self.action.addModifier(0, Modifier('aa'))
        self.action.addModifier(1, Modifier('bb'))
        self.action.addNote(0, "note 1")
        self.action.addNote(0, "note 2")
        self.action.addNote(0, "note 3")
        self.action.setNotes(1, ["note 1", "note 2", "note 3"])
        self.action.setPhaseFrames(0,  1)
        self.action.setPhaseFrames(1,  2)
        self.overview.addAction(self.action)

    def testFormattingAction(self):
        formatter = ActionFormatter(self.overview, self.action)
        data = formatter.format()
        # name, hit, frames, phase, def, aa, bb, cc, notes 1, notes 2, notes 3
        result = [
            ['attack 1', '', '1', '0', 'x', 'x', '', '', 'note 1', 'note 2', 'note 3'],
            ['attack 1', 'x', '2', '1', 'x', '', 'x', '', 'note 1', 'note 2', 'note 3']
        ]
        self.assertEqual(data, result)
