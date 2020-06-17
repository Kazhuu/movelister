class DetailFormatter:
    """
    Class responsible for formatting Detail class instance to two
    dimensional array.
    """
    def __init__(self, detail, modifiersOrdering):
        """
        Construct Detail class formatter. modifiersOrdering is a list of
        modifiers names which is used for ordering modifier combinations. List
        index is used as a sorting key.
        """
        self.detail = detail
        self.modifiersOrdering = modifiersOrdering

    def format(self):
        data = []
        for input_name in self.detail.inputs:
            data.append(self._formatRow(input_name))
        return data

    def _formatRow(self, input_name):
        row = []
        # Action Name
        row.append(self.detail.action.name)
        # Modifiers
        row.append(self._formatModifiers(self.detail.modifiers))
        # Input to Compare
        row.append(input_name)
        # Phases
        input_phases = self.detail.phases.get(input_name, {})
        phase_numbers = list(input_phases.keys())
        # Loop phase number in sorted order.
        for phase_number in sorted(phase_numbers):
            row.extend(input_phases[phase_number])
        # for phase_number, values in self.detail.phases.get(input_name, {}).items():
        # Notes
        row.extend(self.detail.notes.get(input_name, ['']))
        return row

    def _formatModifiers(self, modifiers):
        names = [modifier.name for modifier in modifiers]
        # Sort modifiers according to given modifiers list index.
        names.sort(key=lambda name: self.modifiersOrdering.index(name))
        return ' '.join(names)
