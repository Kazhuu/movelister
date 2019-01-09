from .sheet import Sheet
from . import helper
from movelister.core import cursor
from movelister.model import Modifier


class Modifiers:

    def __init__(self, sheetName):
        self.name = sheetName
        self.sheet = Sheet.getByName(sheetName)
        self.data = cursor.getSheetContent(self.sheet)
        self.headerRowIndex = helper.getHeaderRowPosition(self.data)
        self.dataBeginRow = self.headerRowIndex + 1
        self.nameColumnIndex = helper.getColumnPosition(self.data, 'Short Name')
        self.colorColumnIndex = helper.getColumnPosition(self.data, 'Color')
        self.notColumnIndex = helper.getColumnPosition(self.data, 'NOT')
        self.mathColumnIndex = helper.getColumnPosition(self.data, 'Math')
        self.chainColumnIndex = helper.getColumnPosition(self.data, 'Chain')
        self.dataHeader = self.data[self.headerRowIndex]
        self.dataRows = self.data[self.dataBeginRow:]
        self.modifierColors = helper.getCellColorsFromColumn(self.sheet, self.colorColumnIndex, self.dataBeginRow, len(self.data))

    def getModifiers(self):
        modifiers = []
        for index, row in enumerate(self.dataRows):
            if self._isValidRow(row):
                modifiers.append(Modifier(**self._modifierKwargs(row, index)))
        return modifiers

    def _isValidRow(self, row):
        return row[self.nameColumnIndex] != ''

    def _modifierKwargs(self, row, index):
        kwargs = {'name': row[self.nameColumnIndex]}
        kwargs['color'] = self.modifierColors[index]
        return kwargs
