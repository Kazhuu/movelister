from movelister.model.result import Result
import re


class Detail:

    def __init__(self, action, modifiers):
        self.action = action
        self._inputs = []
        self._phases = {}
        self._notes = {}
        self._modifiers = modifiers

    @property
    def modifiers(self):
        return self._modifiers

    @modifiers.setter
    def modifiers(self, modifiers):
        self._modifiers = modifiers

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        self._inputs = inputs

    @property
    def phases(self):
        return self._phases

    @phases.setter
    def phases(self, phases):
        self._phases = phases

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, notes):
        self._notes = notes

    def getInputResults(self, inputName):
        """
        Return list of Result instances for given input name. List index
        represents phase and Result instance results of that phase. If not
        found empty list is returned instead.

        Input name must exist on this detail if not error is raised.
        """
        if inputName not in self.inputs:
            raise KeyError('input name "{0}" is not part of detail inputs {1}'.format(inputName, self.inputs))
        results = self.phases.get(inputName, None)
        # If this input does not have Result instances yet, then create empty ones.
        if not results:
            results = [Result('', '', '') for _ in range(self.action.phases)]
            self.phases[inputName] = results
        # If this Detail has more phases than previous one read from Details
        # sheet, then fill the gap with empty Result instances.
        if len(results) < self.action.phases:
            remaining = self.action.phases - len(results)
            self.phases[inputName].extend([Result('', '', '') for _ in range(remaining)])
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
