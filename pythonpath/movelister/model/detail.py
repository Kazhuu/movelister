class Detail:

    def __init__(self, action, modifiers, inputs=[], phases={}, notes={}):
        self.action = action
        self.inputs = inputs
        self._modifiers = modifiers
        self.phases = phases
        self.notes = notes

    @property
    def modifiers(self):
        return self._modifiers

    @modifiers.setter
    def modifiers(self, modifiers):
        self._modifiers = modifiers

    def modifiersAsDict(self):
        return {modifier.name: True for modifier in self.modifiers}

    def __eq__(self, other):
        """
        Test object equality. Compares both action name and modifier name.
        """
        s = '-'
        selfName = s.join(self.action, self.modifiers)
        otherName = s.join(other.action, other.modifiers)
        return selfName == otherName

    def __ne__(self, other):
        """
        Test object nonequality.
        """
        return not self == other
