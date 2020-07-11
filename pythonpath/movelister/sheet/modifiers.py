import re
from collections import defaultdict

from movelister.sheet.sheet import Sheet
from movelister.sheet import helper
from movelister.core import cursor
from movelister.model.modifier import Modifier


class Modifiers:

    MODIFIER_PATTER = re.compile(r'\b\w+\b')

    def __init__(self, sheetName):
        self.name = sheetName
        self.sheet = Sheet.getByName(sheetName)
        self.data = helper.stripTrailingEmptyRows(cursor.getSheetContent(self.sheet))
        self.headerRowIndex = helper.getHeaderRowPosition(self.data)
        self.dataBeginRow = self.headerRowIndex + 1
        self.dataRows = self._dataRows()
        self.nameColumnIndex = helper.getColumnPosition(self.data, 'Short Name', 0)
        self.colorColumnIndex = helper.getColumnPosition(self.data, 'Color', 2)
        self.booleanEquationColumIndex = helper.getColumnPosition(self.data, 'Filters', 4)
        self.requiredColumIndex = helper.getColumnPosition(self.data, 'Required', 5)
        self.booleanEquations = self._parseEquations()
        self.dataHeader = self.data[self.headerRowIndex]
        self.dataRows = self.data[self.dataBeginRow:]
        self.modifierColors = helper.getCellColorsFromColumn(
            self.sheet, self.colorColumnIndex, self.dataBeginRow, len(self.data))

    def getModifiers(self):
        modifiers = []
        for index, row in enumerate(self.dataRows):
            if self._isValidRow(row):
                modifiers.append(Modifier(**self._modifierKwargs(row, index)))
        return modifiers

    def isValidDetail(self, detail):
        # TODO: Move this functionality out of this class.
        # This details is a default instance without any modifiers. So this is
        # always a valid case.
        if not detail.modifiers:
            return True
        equations = self._filterEquations(detail)
        # If equation is not found for this detail then it's considered valid.
        if not list(equations):
            return True
        # Evaluate all equations. All of the filtered equations must return
        # true for this detail to be valid.
        results = [eval(self._substituteEquation(equation, detail), self._evalContext()) for equation in equations]
        return all(results)

    def _filterEquations(self, detail):
        pattern = detail.modifiersAsRegExp()
        equations = []
        for equationPair in self.booleanEquations:
            if equationPair[1] | bool(pattern.search(equationPair[0])):
                equations.append(equationPair[0])
        return equations

    def _dataRows(self):
        data = self.data[self.dataBeginRow:]
        return helper.stripTrailingEmptyRows(data)

    def _parseEquations(self):
        equations = []
        for row in self.dataRows:
            if row[self.booleanEquationColumIndex]:
                required = bool(row[self.requiredColumIndex])
                equation = row[self.booleanEquationColumIndex]
                equations.append((equation, required))
        return equations

    def _isValidRow(self, row):
        return row[self.nameColumnIndex] != ''

    def _modifierKwargs(self, row, index):
        kwargs = {'name': row[self.nameColumnIndex]}
        kwargs['color'] = self.modifierColors[index]
        return kwargs

    def _evalContext(self):
        """
        Supported functions for the user in boolean equations.
        """
        def xor(*args):
            return sum(args) == 1
        def neg(result):
            return not result
        context = {
            'xor': xor,
            'neg': neg
        }
        return context

    def _substituteEquation(self, equation, detail):
        # TODO: Move this functionality out of this class.
        # Create dict which returns True if modifier is as a key and False when not.
        mods = defaultdict(bool, detail.modifiersAsDict())
        # Add supported functions.
        mods['xor'] = 'xor'
        mods['neg'] = 'neg'
        # Substitute modifiers in equation with True and False words.
        return re.sub(Modifiers.MODIFIER_PATTER, lambda m: str(mods[m.group(0)]), equation)
