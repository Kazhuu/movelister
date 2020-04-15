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
        filteredData = filter.filterRows(lambda row: row[self.nameColumnIndex] != '', self.dataRows)
        # Create an unused action to the array so that the loop can register all legit actions.
        emptyRow = helper.createEmptyRow(len(filteredData[0]))
        emptyRow[self.nameColumnIndex] = 'Unused'
        emptyRow[self.inputToCompareColumnIndex] = 'Unused'
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
        This function goes through rows to parse everything that belongs to a single Detail,
        then returns the data inside a Detail object.
        """
        # collect Input column.
        inputList = []
        for line in data:
            inputList.append(line[2])
        # collect everything from the phases. Data won't be ordered.
        phasesList = {}
        notesList = {}
        for line in data:
            phaseNum = -1
            cellNum = 2
            counter = -1
            for cell in line:
                counter = counter + 1
                cellNum = cellNum + 1
                # stops the loop and gathers notes-related data once the phases end.
                if cellNum == self.notesIndex1:
                    notesList[line[2]] = [line[self.notesIndex1], line[self.notesIndex2], line[self.notesIndex3]]
                    break
                # ensures the data is taken from the first column of a phase.
                if counter == 3:
                    counter = 0
                # takes data from the three cells of a single phase and places them in a list inside the dict.
                if counter == 0:
                    phaseNum = phaseNum + 1
                    if line[2] not in phasesList:
                        phasesList[line[2]] = {}
                    phasesList[line[2]][str(phaseNum)] = [line[cellNum], line[cellNum + 1], line[cellNum + 2]]
        kwargs = {'action': data[0][self.nameColumnIndex], 'modifiers': data[0][self.modifiersColumnIndex],
                  'inputs': inputList, 'phases': phasesList, 'notes': notesList}
        return Detail(**kwargs)
