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
        row.append(self.detail.action)
        # Modifiers
        row.append(self.detail.modifiers)
        # Input to Compare
        row.append(input_name)
        # Phases
        for phase_number, values in self.detail.phases[input_name].items():
            row.extend(values)
        # Notes
        row.extend(self.detail.notes[input_name])
        return row
