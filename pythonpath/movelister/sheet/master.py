from movelister import cursor
from movelister.sheet import Sheet
from movelister.action import Action


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

    def getAllActions(self):
        actions = []
        for row in self.dataRows:
            if row[NAME_COLUMN] != '':
                name, kwargs = self._rowToKwargs(row)
                actions.append(Action(name, **kwargs))
        return actions

    def getActions(self, viewName):
        actions = []
        for row in self.dataRows:
            if row[VIEW_COLUMN] == viewName:
                name, kwargs = self._rowToKwargs(row)
                actions.append(Action(name, **kwargs))
        return actions

    def _rowToKwargs(self, row):
        kwargs = {}
        if row[INPUTS_COLUMN] != '':
            kwargs['inputs'] = row[INPUTS_COLUMN]
        if row[COLOR_COLUMN] != '':
            kwargs['color'] = row[COLOR_COLUMN]
        if row[PHASE_COLUMN] != '':
            kwargs['phases'] = int(row[PHASE_COLUMN])
        return [row[NAME_COLUMN], kwargs]
