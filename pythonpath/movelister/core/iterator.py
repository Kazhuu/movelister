from itertools import chain, combinations


class ActionsIterator:
    """
    Iterator class to iterate over all possible combinations of given actions
    and their modifiers.

    TODO: Combinations exists but they are not used during iteration. Generate
    Detail class instances from modifier combinations and use them on next()
    method.
    """
    def __init__(self, actions):
        self.actions = actions
        self.index = 0
        self.build_combinations(actions)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            action = self.actions[self.index]
            self.index += 1
            return action
        except IndexError:
            raise StopIteration

    def build_combinations(self, actions):
        self.combinations = iter([])
        for action in actions:
            # If action has default input then add empty modifier combination.
            if action.default:
                chain(self.combinations, combinations([], 1))
            # Add rest of the modifier combinations.
            for phase in range(action.phases):
                names = action.modifierNamesAsList(phase)
                for i in range(1, len(names) + 1):
                    self.combinations = chain(self.combinations, combinations(names, i))
