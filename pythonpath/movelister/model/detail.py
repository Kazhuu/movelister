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

    def modiferNames(self):
        return [modifier.name for modifier in self._modifiers]

    def modifiersAsDict(self):
        return {modifier.name: True for modifier in self.modifiers}

    def modifiersAsRegExp(self):
        names = [modifier.name for modifier in self._modifiers]
        return re.compile(r'[' + '|'.join(names) + ']')

    def __eq__(self, other):
        """
        Test object equality. Compares both action name and modifier name.
        """
        s = '-'
        selfName = s.join(self.action, ''.join(self.modiferNames()))
        otherName = s.join(other.action, ''.join(other.modiferNames()))
        return selfName == otherName

    def __ne__(self, other):
        """
        Test object nonequality.
        """
        return not self == other
