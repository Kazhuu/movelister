class Result:

    END_MARKER = 'end'

    def __init__(self, result, action, modifiers):
        if Result.END_MARKER in [result, action, modifiers]:
            self.result = ''
            self.action = ''
            self.modifiers = ''
        else:
            self.result = result
            self.action = action
            self.modifiers = modifiers
