from movelister import cursor, messageBox


def getColumnLocation(sheet, columnName):
    columnRow = cursor.getRow(sheet, 0)
    column = -1

    # The loop iterates through the row 0 of chosen List to find where a certain Column is.
    x = -1
    while x < len(columnRow):
        x = x + 1
        if columnRow[x] == columnName:
            column = x
            break

    # Error message if it wasn't found.
    if column == - 1:
        messageBox.createMessage('OK', 'Warning:', "Program couldn't find the column " + columnName + '.')
        exit()

    return column


def getRowLocation(sheet, column, string):
    x = 0
    rowPosition = -1

    # The loop iterates through the rows of a chosen List to find a string from some Row.
    while x < 5000:
        x = x + 1
        if sheet.getCellByPosition(column, x).getString() == string:
            rowPosition = x
            break

    # Error message if it wasn't found.
    if column == - 1:
        messageBox.createMessage('OK', 'Warning:', "Program couldn't find a cell with " + string + '.')
        exit()

    return rowPosition
