from movelister import error
from movelister.core import cursor
from movelister.ui import messageBox


def getHeaderRowPosition(sheetData):
    """
    This function figures out at what position the header row is. This may vary between sheets because of UI.
    The code is simple and basically looks for the first non-empty cell on second column.
    """
    for index, row in enumerate(sheetData):
        if row[1] != '':
            return index
    return 0


def getColumnPosition(sheetData, columnName):
    """
    This function iterates through the header row of a List to find where a chosen Column is.
    """
    headerRowPosition = getHeaderRowPosition(sheetData)

    columnRow = sheetData[headerRowPosition]
    column = -1

    x = -1
    while x < len(columnRow) - 1:
        x = x + 1
        if columnRow[x] == columnName:
            column = x
            break

    # Error message if it wasn't found.
    if column == - 1:
        msg = "Program couldn't find the column {0}.".format(columnName)
        messageBox.createMessage('OK', 'Warning:', msg)
        exit()

    return column


def getRowPosition(sheet, text, column):
    """
    This function iterates through a column to find the location of a cell that contains a chosen string.
    """
    mda = cursor.getSheetContent(sheet)
    row = -1

    x = -1
    while x < len(mda) - 1:
        x = x + 1
        if mda[x][column] == text:
            row = x
            break

    # Error message if it wasn't found.
    if row == - 1:
        messageBox.createMessage('OK', 'Warning:', "Program couldn't find where is " + text + '.')
        exit()

    return row


def getCellColorsFromColumn(sheet, column, top, bottom):
    """
    This function creates an array of CellBackColor values from given column
    and includes cells from top to bottom.
    """
    colors = []
    colorRange = sheet.getCellRangeByPosition(column, top, column, bottom)
    for index in range(0, bottom - top):
        colors.append(colorRange.getCellByPosition(0, index).CellBackColor)
    return colors


def getActiveViewName(document):
    '''
    This function splices the string between () from the current active sheet.
    Used in generating Details view.
    '''
    activeSheet = document.getCurrentController().getActiveSheet()
    activeSheetName = activeSheet.Name

    # A bit of error checking.
    error.sheetNameSplitCheck(activeSheetName)

    splitName1 = activeSheetName.split('(')
    splitName2 = splitName1[1].split(')')

    return splitName2[0]
