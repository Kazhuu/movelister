class DetailFormatter:
    """
    Class responsible for formatting Detail class instance to two
    dimensional array.
    """
    def __init__(self, detail):
        self.detail = detail

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
        for phase_number, values in self.detail.phases.get(input_name, {}).items():
            row.extend(values)
        # Notes
        row.extend(self.detail.notes.get(input_name, ['']))
        return row

    def _formatModifiers(self, modifiers):
        return ' '.join([modifier.name for modifier in modifiers])
