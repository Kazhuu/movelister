from movelister.core import cursor
from .sheet import Sheet


def drawSheet(sheetInstance, position):
    sheet = Sheet.newSheet(sheetInstance.name, position)
    cursor.setSheetContent(sheet, sheetInstance.getSheetContent())
    return sheet
