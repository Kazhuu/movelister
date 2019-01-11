class FormatModifiedAction:

    def __init__(self, overview, modifiedAction):
        self.modifiedAction = modifiedAction
        self.overview = overview

    def format(self):
        data = []
        for phase in range(0, self.modifiedAction.phases):
            data.append(self._formatRow(phase))
        return data

    def _formatRow(self, phase):
        row = []
        row.append(self.modifiedAction.name)
        row.append('x' if self.modifiedAction.hitPhase == phase else '')
        row.append('')
        # modifiers
        phaseModifiers = self.modifiedAction.phaseModifiers(phase)
        for mod in self.overview.modifiers:
            row.append('x' if mod in phaseModifiers else '')
        return row
