from movelister.format.result import ResultFormatter


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
        for inputName in self.detail.inputs:
            data.append(self._formatRow(inputName))
        return data

    def _formatRow(self, inputName):
        row = []
        # Action Name
        row.append(self.detail.action.name)
        # Modifiers
        row.append(self._formatModifiers(self.detail.modifiers))
        # Input to Compare
        row.append(inputName)
        # Phase columns.
        inputResults = self.detail.getInputResults(inputName)
        for result in inputResults:
            row.extend(ResultFormatter.format(result))
        # Notes
        row.extend(self.detail.notes.get(inputName, ['']))
        return row

    def _formatModifiers(self, modifiers):
        names = [modifier.name for modifier in modifiers]
        # Sort modifiers according to given modifiers list index.
        names.sort(key=lambda name: self.modifiersOrdering.index(name))
        return ' '.join(names)
