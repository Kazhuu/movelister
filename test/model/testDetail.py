import unittest
from movelister.model.detail import Detail
from movelister.model.action import Action


class DetailTestCase(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.action = Action('aaa', phases=1)

    def testUnfilledResultsAreFilled(self):
        detail = Detail(self.action, [])
        input_name = 'test'
        detail.inputs = [input_name,]
        results1 = detail.getInputResults(input_name)

        self.assertEqual(len(results1), 1)

        # After modifying amount of phases getInputResults() should fill the
        # gap with empty Result instances.
        detail.action.phases = 2
        results2 = detail.getInputResults(input_name)

        self.assertEqual(len(results2), 2)
