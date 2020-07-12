from movelister.sheet.sheet import Sheet
from movelister.sheet import helper
from movelister.core import cursor
from movelister.format import filter


class About:

    def __init__(self, sheetName):
        self.name = sheetName
        self.sheet = Sheet.getByName(sheetName)
        self.data = cursor.getSheetContent(self.sheet)
        self.dataBeginRow = 2
        self.optionsColumnIndex = 0
        self.generateNamedRangesIndex = helper.getRowPosition(self.data, 'Generate Named Ranges:', self.optionsColumnIndex)
        self.showEntriesAscendingIndex = helper.getRowPosition(self.data, 'Show entries ascending when generating validation:', self.optionsColumnIndex)
        self.OptionsColors = helper.getCellColorsFromColumn(
            self.sheet, 1, self.dataBeginRow, len(self.data)
        )

    def isShowEntriesAscendingOn(self):
        cell = self.sheet.getCellByPosition(1, self.showEntriesAscendingIndex)
        if cell.getString():
            return True
        else:
            return False

    def isGenerateNamedRangesOn(self):
        cell = self.sheet.getCellByPosition(1, self.generateNamedRangesIndex)
        if cell.getString():
            return True
        else:
            return False
