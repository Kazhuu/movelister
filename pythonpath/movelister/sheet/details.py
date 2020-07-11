from .sheet import Sheet
from movelister.core import cursor, names
from movelister.format import filter
from movelister.model.detail import Detail
from movelister.model.action import Action
from movelister.model.modifier import Modifier
from movelister.model.result import Result
from movelister.sheet import helper
from movelister.sheet.master import Master
from movelister.sheet.sheet import MASTER_LIST_SHEET_NAME

import re


class Details:

    def __init__(self, viewName):
        self.name = names.getDetailsName(viewName)
        self.viewName = viewName
        self.details = []

    @classmethod
    def fromSheet(cls, sheetName):
        """
        Build instance of Detail from given sheet name which should represents
        current details sheet.
        """
        instance = cls(names.getViewName(sheetName))
        instance._readSheetContent()
        return instance

    def addDetail(self, detail):
        self.details.append(detail)

    def findDetail(self, seekedDetail):
        """
        Find given details instance from this Details sheet. Return it if it's
        found, otherwise return None.
        """
        return next((detail for detail in self.details if detail == seekedDetail), None)


    def _readSheetContent(self):
        # We need master sheet to get number of phases for each Action in the
        # Detail class. Details sheet doesn't provide enough information.
        self.masterSheet = Master(MASTER_LIST_SHEET_NAME)
        self.sheet = Sheet.getByName(self.name)
        self.data = cursor.getSheetContent(self.sheet)
        self.nameColumnIndex = helper.getColumnPosition(self.data, 'Action Name', 0)
        self.modifiersColumnIndex = helper.getColumnPosition(self.data, 'Modifiers', 1)
        self.inputToCompareColumnIndex = helper.getColumnPosition(self.data, 'Input to Compare', 2)
        self.notesIndex1 = helper.getColumnPosition(self.data, 'Notes 1', 3)
        self.notesIndex2 = helper.getColumnPosition(self.data, 'Notes 2', 4)
        self.notesIndex3 = helper.getColumnPosition(self.data, 'Notes 3', 5)
        self.dataRows = self._dataRows()
        self.details = self._readDetails()

    def _dataRows(self):
        data = self.data[1:]
        return helper.stripTrailingEmptyRows(data)

    def _readDetails(self):
        # If details sheet is empty return.
        if not self.dataRows:
            return []
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
        return details

    def _parseArrayIntoDetail(self, data):
        """
        This function goes through rows to parse everything that belongs to a single Detail,
        then returns the data inside a Detail object.
        """
        # TODO: Clean this up to separate functions.
        # collect Input column.
        inputList = []
        for line in data:
            inputList.append(line[2])
        # collect everything from the phases. Data won't be ordered.
        phasesList = {}
        notesList = {}
        for line in data:
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
                    if line[2] not in phasesList:
                        phasesList[line[2]] = []
                    phasesList[line[2]].append(Result(line[cellNum], line[cellNum + 1], line[cellNum + 2]))
        modifiers = self._parseModifiers(data[0][self.modifiersColumnIndex])
        action = self.masterSheet.findAction(self.viewName, data[0][self.nameColumnIndex])
        detail = Detail(action, modifiers)
        detail.inputs = inputList
        detail.phases = phasesList
        detail.notes = notesList
        return detail

    def _parseModifiers(self, modifierCell):
        """
        Parse string of modifier names to list of Modifier instances.
        For example 'WPN1 WPN2' will be two Modifier instances.
        """
        modifiers = []
        pattern = re.compile(r'\b\w+\b')
        for name in re.findall(pattern, modifierCell):
            modifiers.append(Modifier(name))
        return modifiers
