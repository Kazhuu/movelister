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
        return data

    def _formatRow(self, phase):
        row = []
        # Action Name
        row.append(self.detail.action)
        # Modifiers
        row.append(self.detail.modifiers)
        # Input to Compare
        row.append(self.detail.inputs)
        return row
