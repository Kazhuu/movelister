from itertools import chain, combinations

from movelister.model import Detail


class DetailsIterator:
    """
    Iterator class to iterate over all possible combinations of given actions
    and their modifiers. On each iteration Detail class instance is constructed
    and returned.
    """
    def __init__(self, actions):
        self.actions = actions
        self.index = 0
        self.current_action = None
        self.combinations = iter([])

    def __iter__(self):
        return self

    def __next__(self):
        try:
            modifiers = self.combinations.__next__()
            return Detail(self.current_action, modifiers=modifiers)
        except StopIteration:
            try:
                self.current_action = self.actions[self.index]
                self.index += 1
                self.combinations = self.build_modifier_combinations(self.current_action)
                return Detail(self.current_action, modifiers=self.combinations.__next__())
            except IndexError:
                raise StopIteration

    def build_modifier_combinations(self, action):
        mod_combinations = iter([])
        # If action has default input then add empty modifier combination.
        if action.default:
            chain(mod_combinations, combinations([], 1))
        # Add rest of the modifier combinations.
        for phase in range(action.phases):
            names = action.modifierNamesAsList(phase)
            for i in range(1, len(names) + 1):
                mod_combinations = chain(mod_combinations, combinations(names, i))
        return mod_combinations
