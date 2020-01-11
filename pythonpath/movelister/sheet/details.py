from .sheet import Sheet
from movelister.core import cursor
from movelister.sheet import helper


class Details:

    def __init__(self, sheetName):
        self.name = sheetName
        self.details = []

    @classmethod
    def fromSheet(cls, sheetName):
        instance = cls(sheetName)
        instance._readSheetContent()
        return instance

    def _readSheetContent(self):
        self.sheet = Sheet.getByName(self.name)
        self.data = cursor.getSheetContent(self.sheet)
        self.nameColumnIndex = helper.getColumnPosition(self.data, 'Action Name')
        self.modifiersColumIndex = helper.getColumnPosition(self.data, 'Modifiers')
        self.inputToCompareColumIndex = helper.getColumnPosition(self.data, 'Input to Compare')
        self.dataRows = self._dataRows()

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
