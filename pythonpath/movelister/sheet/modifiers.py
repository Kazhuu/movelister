import re
from collections import defaultdict

from movelister.sheet.sheet import Sheet
from movelister.sheet import helper
from movelister.core import cursor
from movelister.model.modifier import Modifier


class Modifiers:

    def __init__(self, sheetName):
        self.name = sheetName
        self.sheet = Sheet.getByName(sheetName)
        self.data = helper.stripTrailingEmptyRows(cursor.getSheetContent(self.sheet))
        self.headerRowIndex = helper.getHeaderRowPosition(self.data)
        self.dataBeginRow = self.headerRowIndex + 1
        self.dataRows = self._dataRows()
        self.nameColumnIndex = helper.getColumnPosition(self.data, 'Short Name')
        self.colorColumnIndex = helper.getColumnPosition(self.data, 'Color')
        self.booleanEquationColumIndex = helper.getColumnPosition(self.data, 'Filters')
        self.booleanEquations = self._getEquations()
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
        for equation in self.booleanEquations:
            print(self._substituteEquation(equation, detail))
            print(eval(self._substituteEquation(equation, detail)))
            if eval(self._substituteEquation(equation, detail)):
                return True
        return False

    def _dataRows(self):
        data = self.data[self.dataBeginRow:]
        return helper.stripTrailingEmptyRows(data)

    def _getEquations(self):
        equations = []
        for row in self.dataRows:
            if row[self.booleanEquationColumIndex]:
                equations.append(row[self.booleanEquationColumIndex])
        return equations

    def _isValidRow(self, row):
        return row[self.nameColumnIndex] != ''

    def _modifierKwargs(self, row, index):
        kwargs = {'name': row[self.nameColumnIndex]}
        kwargs['color'] = self.modifierColors[index]
        return kwargs

    def _substituteEquation(self, equation, detail):
        # Create dict which returns True if modifier is as a key and False when not.
        mods = defaultdict(bool, detail.modifiersAsDict())
        modifier_pattern = r'\b\w+\b'
        # Substitute modifiers in equation with True and False words.
        return re.sub(modifier_pattern, lambda m: str(mods[m.group(0)]), equation)
