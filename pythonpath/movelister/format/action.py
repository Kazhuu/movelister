class ActionFormatter:
    """
    Class responsible for formatting Action class instance to two
    dimensional array.
    """

    def __init__(self, overview, action, padding=0):
        self.action = action
        self.overview = overview
        self.padding = padding

    def format(self):
        data = []
        for phase in range(0, self.action.phases):
            data.append(self._formatRow(phase))
        return data

    def _formatRow(self, phase):
        row = []
        # name
        row.append(self.action.name)
        # hit
        if self.action.hitPhase is not None:
            row.append('x' if self.action.hitPhase - 1 == phase else '')
        else:
            row.append('')
        # frames
        row.append('')
        # phase number
        row.append(str(phase))
        # default
        row.append('x' if self.action.default else '')
        # modifiers
        phaseModifiers = self.action.phaseModifiers(phase)
        for mod in self.overview.modifiers:
            row.append('x' if mod in phaseModifiers else '')
        # padding to fill cells without content
        return row + ['' for _ in range(0, self.padding)]
