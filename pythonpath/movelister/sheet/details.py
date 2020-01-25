from .sheet import Sheet
from movelister.core import cursor
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
        return self._stripTrailingEmptyRows(data)

    def _stripTrailingEmptyRows(self, data):
        """
        TODO: Refactor this code to one place. Also exists in sheet.Overview class.
        """
        endIndex = len(data)
        for index, row in reversed(list(enumerate(data))):
            if row[0] == '':
                endIndex = endIndex - 1
            else:
                break
        return data[:endIndex]

    def _readDetails(self):
        details = []
        print()
