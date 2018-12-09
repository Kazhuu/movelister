from movelister.core import cursor
from .sheet import Sheet


class Overview:

    def __init__(self):
        pass

    @classmethod
    def fromSheet(cls, sheetName):
        instance = cls()
        instance.readSheetContent(sheetName)
        return instance

    def readSheetContent(self, sheetName):
        self.name = sheetName
        self.sheet = Sheet.getByName(sheetName)
        self.data = cursor.getSheetContent(self.sheet)
