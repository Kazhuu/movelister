class ModifiedActionFormatter:
    """
    Class responsible formatting ModifiedAction class intance to two
    dimensional array.
    """

    def __init__(self, overview, modifiedAction, padding=0):
        self.modifiedAction = modifiedAction
        self.overview = overview
        self.padding = padding

    def format(self):
        data = []
        for phase in range(0, self.modifiedAction.phases):
            data.append(self._formatRow(phase))
        return data

    def _formatRow(self, phase):
        row = []
        # name
        row.append(self.modifiedAction.name)
        # hit
        row.append('x' if self.modifiedAction.hitPhase - 1 == phase else '')
        # frames
        row.append('')
        # phase number
        row.append(str(phase))
        # default
        row.append('x' if self.modifiedAction.default else '')
        # modifiers
        phaseModifiers = self.modifiedAction.phaseModifiers(phase)
        for mod in self.overview.modifiers:
            row.append('x' if mod in phaseModifiers else '')
        # padding to fill cells without content
        return row + ['' for _ in range(0, self.padding)]
