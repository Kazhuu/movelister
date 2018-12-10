from .sheet import Sheet
from . import helper
from movelister.core import cursor
from movelister.model import Input
from movelister.format import filter


HEADER_ROW = 0
DATA_BEGIN_ROW = 1

INPUT_LIST_NAME_COLUMN = 0
NAME_COLUMN = 1
INPUT_GROUP_COLUMN = 2
COLOR_COLUMN = 4


class Inputs:

    def __init__(self, sheetName):
        self.name = sheetName
        self.sheet = Sheet.getByName(sheetName)
        self.data = cursor.getSheetContent(self.sheet)
        self.dataHeader = self.data[HEADER_ROW]
        self.dataRows = self.data[DATA_BEGIN_ROW:]
        self.inputColors = helper.getCellColorsFromColumn(self.sheet, COLOR_COLUMN, DATA_BEGIN_ROW, len(self.data))

    def getInputList(self, name):
        inputGroup = []
        rows = filter.filterRows(lambda row: row[INPUT_LIST_NAME_COLUMN] == name, self.dataRows)
        for index, row in enumerate(rows):
            if self._isValidRow(row):
                kwargs = self._rowToKwargs(row)
                kwargs['color'] = self.inputColors[index]
                inputGroup.append(Input(**kwargs))
        return inputGroup

    def _isValidRow(self, row):
        return row[NAME_COLUMN] != ''

    def _rowToKwargs(self, row):
        kwargs = {'name': row[NAME_COLUMN]}
        if row[INPUT_GROUP_COLUMN] != '':
            kwargs['group'] = row[INPUT_GROUP_COLUMN]
        return kwargs
