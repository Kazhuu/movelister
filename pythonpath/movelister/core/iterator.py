from itertools import chain, combinations

from movelister.model.detail import Detail
from movelister.sheet.inputs import Inputs
from movelister.sheet.sheet import INPUT_LIST_SHEET_NAME, MODIFIER_LIST_SHEET_NAME
from movelister.sheet.modifiers import Modifiers


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
        self.ordering = Modifiers(MODIFIER_LIST_SHEET_NAME).getModifiers()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            modifiers = self.combinations.__next__()
            inputs = self.inputsSheet.getInputNames(self.currentAction.inputs)
            return Detail(self.currentAction, inputs=inputs, modifiers=modifiers)
        except StopIteration:
            try:
                self.index = self.nextIndex()
                self.currentAction = self.actions[self.index]
                self.index += 1
                self.combinations = self.buildModifierCombinations(self.currentAction)
                inputs = self.inputsSheet.getInputNames(self.currentAction.inputs)
                return Detail(self.currentAction, inputs=inputs, modifiers=self.combinations.__next__())
            except IndexError:
                raise StopIteration

    def nextIndex(self):
        for index in range(self.index, len(self.actions)):
            action = self.actions[index]
            if action.validAction():
                return index
        return len(self.actions)

    def buildModifierCombinations(self, action):
        modCombinations = iter([])
        # If action has default input then add empty modifier combination.
        if action.default:
            modCombinations = chain(modCombinations, combinations([], 0))
        # Add rest of the modifier combinations.
        modifiers = action.getModifiersSet(self.ordering)
        for i in range(1, len(modifiers) + 1):
            modCombinations = chain(modCombinations, combinations(modifiers, i))
        return modCombinations
