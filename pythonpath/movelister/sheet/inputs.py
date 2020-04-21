from movelister.sheet.sheet import Sheet
from movelister.sheet import helper
from movelister.core import cursor
from movelister.model.input import Input
from movelister.format import filter


class Inputs:

    def __init__(self, sheetName):
        self.name = sheetName
        self.sheet = Sheet.getByName(sheetName)
        self.data = cursor.getSheetContent(self.sheet)
        self.headerRowIndex = helper.getHeaderRowPosition(self.data)
        self.dataBeginRow = self.headerRowIndex + 1
        self.inputsColumnIndex = helper.getColumnPosition(self.data, 'Input List')
        self.nameColumnIndex = helper.getColumnPosition(self.data, 'Input Name')
        self.buttonColumnIndex = helper.getColumnPosition(self.data, 'Button')
        self.inputGroupIndex = helper.getColumnPosition(self.data, 'Group')
        self.colorColumnIndex = helper.getColumnPosition(self.data, 'Color')
        self.dataHeader = self.data[self.headerRowIndex]
        self.dataRows = self.data[self.dataBeginRow:]
        self.inputColors = helper.getCellColorsFromColumn(
            self.sheet, self.colorColumnIndex, self.dataBeginRow, len(self.data)
        )

    def getInputs(self, listName=None):
        """
        Return list of Input class instances.
        """
        inputs = []
        rows = self.dataRows
        if listName:
            rows = filter.filterRows(lambda row: row[self.inputsColumnIndex] == listName, self.dataRows)
        for index, row in enumerate(rows):
            if self._isValidRow(row):
                kwargs = self._rowToKwargs(row)
                kwargs['color'] = self.inputColors[index]
                inputs.append(Input(**kwargs))
        return inputs

    def _isValidRow(self, row):
        return row[self.nameColumnIndex] != ''

    def _rowToKwargs(self, row):
        kwargs = {'name': row[self.nameColumnIndex]}
        if row[self.inputGroupIndex] != '':
            kwargs['group'] = row[self.inputGroupIndex]
        return kwargs
