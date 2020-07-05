import re


class Detail:

    def __init__(self, action, modifiers, inputs=[], phases={}, notes={}):
        self.action = action
        self.inputs = inputs
        self.phases = phases
        self.notes = notes
        self._modifiers = modifiers

    @property
    def modifiers(self):
        return self._modifiers

    @modifiers.setter
    def modifiers(self, modifiers):
        self._modifiers = modifiers

    def getInputResults(self, inputName):
        return self.phases[inputName]

    def modiferNames(self):
        return [modifier.name for modifier in self._modifiers]

    def modifiersAsDict(self):
        return {modifier.name: True for modifier in self.modifiers}

    def modifiersAsRegExp(self):
        names = [modifier.name for modifier in self._modifiers]
        return re.compile(r'(?:' + '|'.join(r'\b{0}\b'.format(name) for name in names) + ')')

    def __eq__(self, other):
        """
        Test object equality. Compares both action name and modifier name.
        """
        return self._identifierString() == other._identifierString()

    def __ne__(self, other):
        """
        Test object nonequality.
        """
        return not self == other

    def _identifierString(self):
        return '{0} {1}'.format(self.action.name,  ' '.join(self.modiferNames()))
