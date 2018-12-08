from movelister import cursor
from movelister.sheet import Sheet
from movelister.action import Action
from movelister.format import filter


HEADER_ROW = 1
DATA_BEGIN_ROW = 2

VIEW_COLUMN = 0
INPUTS_COLUMN = 1
NAME_COLUMN = 2
COLOR_COLUMN = 3
PHASE_COLUMN = 4


class Master:

    def __init__(self, sheetName):
        self.name = sheetName
        self.sheet = Sheet.getByName(sheetName)
        self.data = cursor.getSheetContent(self.sheet)
        self.dataHeader = self.data[HEADER_ROW]
        self.dataRows = self.data[DATA_BEGIN_ROW:]
        self.actionColors = self._getActionColors()

    def getActions(self, view=None):
        actions = []
        rows = self.dataRows
        if view:
            rows = filter.filterRows(lambda row: row[VIEW_COLUMN] == view, self.dataRows)
        for index, row in enumerate(rows):
            if self._isValidRow(row):
                name, kwargs = self._rowToKwargs(row)
                kwargs['color'] = self.actionColors[index]
                actions.append(Action(name, **kwargs))
        return actions

    def _isValidRow(self, row):
        return row[NAME_COLUMN] != ''

    def _rowToKwargs(self, row):
        kwargs = {}
        if row[INPUTS_COLUMN] != '':
            kwargs['inputs'] = row[INPUTS_COLUMN]
        if row[PHASE_COLUMN] != '':
            kwargs['phases'] = int(row[PHASE_COLUMN])
        return [row[NAME_COLUMN], kwargs]

    def _getActionColors(self):
        colors = []
        colorRange = self.sheet.getCellRangeByPosition(COLOR_COLUMN, DATA_BEGIN_ROW, COLOR_COLUMN, len(self.data))
        for index, row in enumerate(self.dataRows):
            colors.append(colorRange.getCellByPosition(0, index).CellBackColor)
        return colors
