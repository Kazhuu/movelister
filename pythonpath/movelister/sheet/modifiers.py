from .base import BaseSheet


HEADER_ROW = 0
DATA_BEGIN_ROW = 1

NAME_COLUMN = 2


class Modifiers(BaseSheet):

    def __init__(self, sheetName):
        super().__init__(sheetName)
        self.dataHeader = self.data[HEADER_ROW]
        self.dataRows = self.data[DATA_BEGIN_ROW:]

    def getModifiers(self):
        modifiers = []
        for row in self.dataRows:
            if row[NAME_COLUMN] != '':
                modifiers.append(row[NAME_COLUMN])
        return modifiers
