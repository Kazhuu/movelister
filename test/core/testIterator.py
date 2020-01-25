from test import OfficeTestCase
from movelister.core.iterator import DetailsIterator
from movelister.model import Action, Modifier


class ActionsIteratorTestCase(OfficeTestCase):

    def setUp(self):
        self.names = ['test1', 'test2', 'test3']
        self.actions = [Action(name) for name in self.names]
        self.actions[1].default = True
        self.actions[0].setModifiers(0, [Modifier('mod1'), Modifier('mod2')])

    def testIteratingDetail(self):
        for index, detail in enumerate(DetailsIterator(self.actions[:0])):
            self.assertEqual(action.name, self.names[index])

    def testFilteringActions(self):
        filteredActions = filter(lambda action: action.name == self.names[0], DetailsIterator(self.actions))
        filteredActions = list(filteredActions)
        self.assertEqual(len(filteredActions), 1)
        self.assertListEqual(filteredActions, self.actions[:1])
