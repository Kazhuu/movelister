class DetailFormatter:
    """
    Class responsible for formatting Detail class instance to two
    dimensional array.

    TODO: write code.
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
        # Phases TO DO
        row.append(self.detail.phases[self.detail.inputs][0])
        # Notes TO DO
        row.append(self.detail.notes[self.detail.inputs][0])
        return row
