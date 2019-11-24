from movelister.core import cursor
from .sheet import Sheet
from . import helper
from movelister.model import Action, ModifiedAction
from movelister.format import filter


class Master:

    def __init__(self, sheetName):
        self.name = sheetName
        self.sheet = Sheet.getByName(sheetName)
        self.data = cursor.getSheetContent(self.sheet)
        self.headerRowIndex = helper.getHeaderRowPosition(self.data)
        self.dataBeginRow = self.headerRowIndex + 1
        self.viewColumnIndex = helper.getColumnPosition(self.data, 'View')
        self.inputsColumnIndex = helper.getColumnPosition(self.data, 'Input List')
        self.nameColumnIndex = helper.getColumnPosition(self.data, 'Action Name')
        self.colorColumnIndex = helper.getColumnPosition(self.data, 'Color')
        self.phaseColumnIndex = helper.getColumnPosition(self.data, 'Phases')
        self.dataHeader = self.data[self.headerRowIndex]
        self.dataRows = self.data[self.dataBeginRow:]
        self.actionColors = helper.getCellColorsFromColumn(
            self.sheet, self.colorColumnIndex, self.dataBeginRow, len(self.data))

    def getActions(self, view=None):
        return self.getModifiedActions(view)

    def getModifiedActions(self, view=None):
        actions = []
        rows = self.dataRows
        if view:
            rows = filter.filterRows(lambda row: row[self.viewColumnIndex] == view, self.dataRows)
        for index, row in enumerate(rows):
            if self._isValidRow(row):
                kwargs = self._rowToKwargs(row)
                kwargs['color'] = self.actionColors[index]
                actions.append(ModifiedAction(**kwargs))
        return actions

    def getOverviewName(self):
        """
        Return name from user input field on Master List sheet.
        """
        name = self.data[0][2]
        return name

    def _isValidRow(self, row):
        return row[self.nameColumnIndex] != ''

    def _rowToKwargs(self, row):
        kwargs = {'name': row[self.nameColumnIndex]}
        if row[self.inputsColumnIndex] != '':
            kwargs['inputs'] = row[self.inputsColumnIndex]
        if row[self.phaseColumnIndex] != '':
            kwargs['phases'] = int(row[self.phaseColumnIndex])
        return kwargs
