from movelister.core import cursor
from movelister.sheet import Sheet


def generateSheet(sheetInstance, position):
    sheet = Sheet.newSheet(sheetInstance.name, position)
    cursor.setSheetContent(sheet, sheetInstance.getSheetContent())
    return sheet
