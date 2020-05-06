class DetailFormatter:
    """
    Class responsible for formatting Detail class instance to two
    dimensional array.
    """

    def __init__(self, detail):
        self.detail = detail

    def format(self):
        data = []
        for line in self.detail:
            data.append()
        return data

    def _formatRow(self):
        row = []
        # Action Name
        row.append(self.detail.action)
        # Modifiers
        row.append(self.detail.modifiers)
        # Input to Compare
        row.append(self.detail.inputs)
        # Phases
        x = -1
        while x < len(self.detail.phases[self.detail.inputs] + 1):
            x = x + 1
            if x in self.detail.phases[self.detail.inputs]:
                for cell in self.detail.phases[self.detail.inputs][x]:
                    row.append(cell)
        # Notes
        for cell in self.detail.notes[self.detail.inputs]:
            row.append(cell)
        return row
