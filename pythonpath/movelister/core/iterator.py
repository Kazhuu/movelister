from itertools import chain, combinations

from movelister.model.detail import Detail
from movelister.sheet.inputs import Inputs
from movelister.sheet.sheet import INPUT_LIST_SHEET_NAME


class DetailsIterator:
    """
    Iterator class to iterate over all possible combinations of given actions
    and their modifiers. On each iteration Detail class instance is constructed
    and returned.
    """
    def __init__(self, actions):
        self.actions = actions
        self.index = 0
        self.currentAction = None
        self.combinations = iter([])
        self.inputsSheet = Inputs(INPUT_LIST_SHEET_NAME)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            modifiers = self.combinations.__next__()
            inputs = self.inputsSheet.getInputNames(self.currentAction.inputs)
            return Detail(self.currentAction, inputs=inputs, modifiers=modifiers)
        except StopIteration:
            try:
                self.currentAction = self.actions[self.index]
                self.index += 1
                self.combinations = self.buildModifierCombinations(self.currentAction)
                inputs = self.inputsSheet.getInputNames(self.currentAction.inputs)
                return Detail(self.currentAction, inputs=inputs, modifiers=self.combinations.__next__())
            except IndexError:
                raise StopIteration

    def buildModifierCombinations(self, action):
        modCombinations = iter([])
        # If action has default input then add empty modifier combination.
        if action.default:
            chain(modCombinations, combinations([], 1))
        # Add rest of the modifier combinations.
        for phase in range(action.phases):
            modifiers = action.getModifiersByPhase(phase)
            for i in range(1, len(modifiers) + 1):
                modCombinations = chain(modCombinations, combinations(modifiers, i))
        return modCombinations
