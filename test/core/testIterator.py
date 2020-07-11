from test.officeTestCase import OfficeTestCase
from movelister.core.iterator import DetailsIterator
from movelister.model.action import Action
from movelister.model.modifier import Modifier


class DetailsIteratorTestCase(OfficeTestCase):

    def setUp(self):
        super().setUp()
        self.names = ['test1', 'test2', 'test3']
        self.actions = [Action(name) for name in self.names]
        self.actions[1].default = True
        self.actions[0].setModifiers(0, [Modifier('WPN1'), Modifier('WPN2')])

    def testIteratingDetail(self):
        for index, detail in enumerate(DetailsIterator(self.actions[:0])):
            self.assertEqual(detail.action.name, self.names[index])

    def testFilteringDetails(self):
        """
        Test that filtered first detail includes all possible modifier combinations.
        """
        filteredDetails = filter(lambda detail: detail.action.name == self.names[0], DetailsIterator(self.actions))
        filteredDetails = list(filteredDetails)
        self.assertEqual(len(filteredDetails), 3)
        self.assertEqual(filteredDetails[0].modifiers, (Modifier('WPN1'),))
        self.assertEqual(filteredDetails[1].modifiers, (Modifier('WPN2'),))
        self.assertEqual(filteredDetails[2].modifiers, (Modifier('WPN1'), Modifier('WPN2')))

    def testDetailsDoNotPointToSameData(self):
        """
        Test that details objects are individual and can be modified separately
        without affecting one another. In other words do not point to same
        underlying data.
        """
        details = list(DetailsIterator(self.actions))
        self.assertIsNot(details[0].phases, details[1].phases)
        self.assertIsNot(details[0].inputs, details[1].inputs)
        self.assertIsNot(details[0].notes, details[1].notes)

