from .action import Action


class ModifiedAction(Action):

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.default = kwargs.get('default', False)
        self.hitPhase = kwargs.get('hitPhase', None)
        self.modifiers = kwargs.get('modifiers', {})

    def setModifiers(self, phase, modifiers):
        self._checkPhaseRange(phase)
        self.modifiers[phase] = modifiers
        return self.modifiers

    def addModifier(self, phase, modifier):
        self._checkPhaseRange(phase)
        try:
            self.modifiers[phase].append(modifier)
        except KeyError:
            self.modifiers[phase] = [modifier]
        return self.modifiers

    def clearModifiers(self, phase):
        self._checkPhaseRange(phase)
        return self.modifiers.pop(phase, [])

    def clearAllModifiers(self):
        self.modifiers = {}

    def _checkPhaseRange(self, phase):
        if phase < 0 or phase > self.phases - 1:
            raise ValueError('phase {0} out of range, must be from 0 to {1}'.format(phase, self.phases - 1))
