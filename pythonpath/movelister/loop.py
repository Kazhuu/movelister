from movelister import cursor, loop, messageBox


def getHeaderRowPosition(sheet):
    """
    This function figures out at what position the header row is. This may vary between sheets
    because of UI. The code is simple and basically looks for the first non-empty cell on first column.
    """
    mda = cursor.getSheetContent(sheet)
    row = -1

    x = -1
    while x < len(mda) - 1:
        x = x + 1
        if mda[x][0] != '':
            row = x
            break

    # Error message if it wasn't found.
    if row == - 1:
        msg = "Program couldn't find the header row from {0}.".format(sheet.getName())
        messageBox.createMessage('OK', 'Warning:', msg)
        exit()

    return row


def getColumnPosition(sheet, columnName):
    """
    This function iterates through the row 0 of a List to find where a certain Column is.

    Known bugs: using cursor to get first row of About-sheet gives an out of bounds exception.
    """
    headerRowPosition = getHeaderRowPosition(sheet)

    columnRow = cursor.getRow(sheet, headerRowPosition)
    column = -1

    x = -1
    while x < len(columnRow) - 1:
        x = x + 1
        if columnRow[x] == columnName:
            column = x
            break

    # Error message if it wasn't found.
    if column == - 1:
        msg = "Program couldn't find the column {0} from {1}".format(columnName, sheet.getName())
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


def getColorArray(sheet):
    """
    This function creates an array of CellBackColor from the Color column in a chosen sheet.
    The loop starts counting from after the position of the header.
    """
    headerRowPosition = getHeaderRowPosition(sheet)

    sheetLength = cursor.getColumn(sheet, 0)
    colPosition = loop.getColumnPosition(sheet, 'Color')
    colorList = []

    x = 0 + headerRowPosition
    while x < len(sheetLength) - 1 + headerRowPosition:
        x = x + 1
        colorList.append(sheet.getCellByPosition(colPosition, x).CellBackColor)

    return colorList
