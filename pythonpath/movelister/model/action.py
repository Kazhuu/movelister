class Action:

    def __init__(self, name, **kwargs):
        if not isinstance(name, str):
            raise ValueError('action must have a name as string')
        self.name = name
        self.inputs = kwargs.get('inputs', 'Default')
        self.color = kwargs.get('color', -1)
        self.phases = kwargs.get('phases', 1)
        self.default = kwargs.get('default', False)
        self.hitPhase = kwargs.get('hitPhase', None)
        self.modifiers = kwargs.get('modifiers', {})
        self.notes = kwargs.get('notes', {})

    def __eq__(self, other):
        """
        Test object equality.
        """
        return self.name == other.name

    def __ne__(self, other):
        """
        Test object nonequality.
        """
        return not self == other

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

    def getModifiersByPhase(self, phase):
        self._checkPhaseRange(phase)
        return self.modifiers.get(phase, [])

    def clearModifiersByPhase(self, phase):
        self._checkPhaseRange(phase)
        return self.modifiers.pop(phase, [])

    def clearAllModifiers(self):
        self.modifiers = {}

    def setNotes(self, phase, notes):
        self._checkPhaseRange(phase)
        self.notes[phase] = notes
        return self.notes

    def addNote(self, phase, notes):
        self._checkPhaseRange(phase)
        try:
            self.notes[phase].append(notes)
        except KeyError:
            self.notes[phase] = [notes]
        return self.notes

    def getNotesByPhase(self, phase):
        self._checkPhaseRange(phase)
        return self.notes.get(phase, [])

    def _checkPhaseRange(self, phase):
        if phase < 0 or phase > self.phases - 1:
            raise ValueError('phase {0} out of range, must be from 0 to {1}'.format(phase, self.phases - 1))
