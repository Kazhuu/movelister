from movelister.format.result import ResultFormatter


class DetailFormatter:
    """
    Class responsible for formatting Detail class instance to two
    dimensional array.
    """

    @classmethod
    def format(cls, detail, modifiersOrdering, maximumPhasesCount):
        """
        Format Detail instance. Given modifiersOrdering is a list of modifiers
        names which is used for ordering modifier combinations. List index is
        used as a sorting key.
        """
        cls.detail = detail
        cls.modifiersOrdering = modifiersOrdering
        cls.maximumPhasesCount = maximumPhasesCount
        data = []
        for inputName in detail.inputs:
            data.append(cls._formatRow(inputName))
        return data

    @classmethod
    def _formatRow(cls, inputName):
        row = []
        # Action Name
        row.append(cls.detail.action.name)
        # Modifiers
        row.append(cls._formatModifiers(cls.detail.modifiers))
        # Input to Compare
        row.append(inputName)
        # Phase columns.
        inputResults = cls.detail.getInputResults(inputName)
        for index in range(cls.detail.action.phases):
            row.extend(ResultFormatter.format(inputResults[index]))
        # Mark end of phases for this action.
        if cls.detail.action.phases < cls.maximumPhasesCount:
            row.extend(['---', '', ''])
        # Fill rest of the cells if any.
        row.extend(['', '', ''] * (cls.maximumPhasesCount - cls.detail.action.phases - 1))
        # Notes
        row.extend(cls.detail.notes.get(inputName, ['']))
        return row

    @classmethod
    def _formatModifiers(cls, modifiers):
        names = [modifier.name for modifier in modifiers]
        # Sort modifiers according to given modifiers list index.
        names.sort(key=lambda name: cls.modifiersOrdering.index(name))
        return ' '.join(names)
