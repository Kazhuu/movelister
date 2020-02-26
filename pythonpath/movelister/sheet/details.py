from .sheet import Sheet
from movelister.core import cursor
from movelister.format import filter
from movelister.model import Detail
from movelister.sheet import helper


class Details:

    def __init__(self, sheetName):
        self.name = sheetName
        self._details = []

    @classmethod
    def fromSheet(cls, sheetName):
        instance = cls(sheetName)
        instance._readSheetContent()
        return instance

    def _readSheetContent(self):
        self.sheet = Sheet.getByName(self.name)
        self.data = cursor.getSheetContent(self.sheet)
        self.nameColumnIndex = helper.getColumnPosition(self.data, 'Action Name')
        self.modifiersColumnIndex = helper.getColumnPosition(self.data, 'Modifiers')
        self.inputToCompareColumnIndex = helper.getColumnPosition(self.data, 'Input to Compare')
        self.notesIndex1 = helper.getColumnPosition(self.data, 'Notes 1')
        self.notesIndex2 = helper.getColumnPosition(self.data, 'Notes 2')
        self.notesIndex3 = helper.getColumnPosition(self.data, 'Notes 3')
        self.dataRows = self._dataRows()
        self._details = self._readDetails()

    def _dataRows(self):
        data = self.data[1:]
        return helper.stripTrailingEmptyRows(data)

    def _readDetails(self):
        currentName = ''
        currentMod = ''
        tempArray = []
        details = []
        # Create an unused action to the array so that the loop can register all legit actions.
        filteredData = filter.filterRows(lambda row: row[self.nameColumnIndex] != '', self.dataRows)
        emptyRow = helper.createEmptyRow(len(filteredData[0]))
        emptyRow[self.nameColumnIndex] = 'Unused'
        filteredData.append(emptyRow)
        # Iterate through filteredData to find out which rows contain relevant data for a single Detail.
        # Then send the relevant rows to _parseArrayIntoDetail function.
        for row in filteredData:
            if row[self.nameColumnIndex] != currentName or row[self.modifiersColumnIndex] != currentMod:
                currentName = row[self.nameColumnIndex]
                currentMod = row[self.modifiersColumnIndex]
                if tempArray != []:
                    details.append(self._parseArrayIntoDetail(tempArray))
                    tempArray = []
                tempArray.append(row)

    def _parseArrayIntoDetail(self, data):
        """
        This function goes through many rows in a table to parse everything that belongs to
        a single Detail, then returns the Detail object.

        TO DO: code should read rest of the values from the array.
        """
        kwargs = {'action': data[0][self.nameColumnIndex], 'modifiers': data[0][self.modifiersColumnIndex]}
        return Detail(**kwargs)
