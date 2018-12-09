from .sheet import Sheet
from movelister.core import cursor


HEADER_ROW = 0
DATA_BEGIN_ROW = 1

NAME_COLUMN = 0


class Modifiers:

    def __init__(self, sheetName):
        self.name = sheetName
        self.sheet = Sheet.getByName(sheetName)
        self.data = cursor.getSheetContent(self.sheet)
        self.dataHeader = self.data[HEADER_ROW]
        self.dataRows = self.data[DATA_BEGIN_ROW:]

    def getModifiers(self):
        modifiers = []
        for row in self.dataRows:
            if row[NAME_COLUMN] != '':
                modifiers.append(row[NAME_COLUMN])
        return modifiers
