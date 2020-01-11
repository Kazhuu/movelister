from test import OfficeTestCase
from movelister.core.iterator import ActionsIterator
from movelister.model import Action


class ActionsIteratorTestCase(OfficeTestCase):

    def setUp(self):
        self.names = ['test1', 'test2', 'test3']
        self.actions = [Action(name) for name in self.names]

    def testIteratingActions(self):
        for index, action in enumerate(ActionsIterator(self.actions)):
            self.assertEqual(action.name, self.names[index])

    def testFilteringActions(self):
        filteredActions = filter(lambda action: action.name == self.names[0], ActionsIterator(self.actions))
        filteredActions = list(filteredActions)
        self.assertEqual(len(filteredActions), 1)
        self.assertListEqual(filteredActions, self.actions[:1])
