class ActionsIterator:
    """
    Iterator class to iterate over given actions.
    """
    def __init__(self, actions):
        self.actions = actions
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            action = self.actions[self.index]
            self.index += 1
            return action
        except IndexError:
            raise StopIteration
