from movelister.core import cursor
from movelister.core.context import Context
from movelister.format import convert
from movelister.sheet.sheet import Sheet
from com.sun.star.sheet.Border import TOP


def createNamedRangesToSheet(sheet, column):
    """
    This function goes through a column in a sheet and assigns Named Ranges based
    on its values to make it easier to move around the sheet. This function is mostly
    intended for Details-sheets, however.

    TODO: switch to deleteFilteredNamedRanges eventually, since otherwise you lose
    named ranges whenever running this function from all except one sheet.
    """
    namedRanges = Context.getDocument().NamedRanges
    sheetData = cursor.getColumn(sheet, 0)

    # Delete previous named ranges.
    deleteNamedRanges(namedRanges)

    currentAction = sheet.getCellByPosition(0, 1).getString()
    startRow = 1

    x = -1
    for line in sheetData[1:]:
        x = x + 1
        if line != currentAction and line != '':
            createNewNamedRange(sheet, currentAction, namedRanges, startRow + 1, x, 1, 1)
            startRow = x
            currentAction = line
        if x == len(sheetData) - 2:
            createNewNamedRange(sheet, currentAction, namedRanges, startRow + 1, x + 1, 1, 1)


def createNewNamedRange(sheet, name, namedRanges, startRow, endRow, startCol, endCol):
    """
    A function that creates a new Named Range based on user requirements.
    """
    col1 = convert.convertIntoBaseAddress(startCol)
    col2 = convert.convertIntoBaseAddress(endCol)
    cellAddress = sheet.getCellByPosition(1, 1).getCellAddress()
    string = '$\'' + sheet.Name + '\'.' + '$' + col1 + '$' + str(startRow) + ':' + '$' + col2 + '$' + str(endRow)
    print(string)
    namedRanges.addNewByName(name, string, cellAddress, 0)


def deleteNamedRanges(namedRanges):
    """
    A function that deletes all named ranges in a document. Probably useful to
    invoke whenever code deletes a sheet with named ranges from the document.
    """
    for item in namedRanges.getElementNames():
        namedRanges.removeByName(item)


def deleteFilteredNamedRanges(namedRanges, sheetName):
    """
    A function that deletes all named ranges from a specific sheet.
    """
    deleteArray = []
    string = '$\'' + sheetName + '\''

    # Filter through namedRanges to find which ranges to delete.
    for item in namedRanges:
        if str(item.getContent()).startswith(string) == True:
            deleteArray.append((str(item.getName())))

    # Delete the ranges.
    for item in deleteArray:
        namedRanges.removeByName(item)
