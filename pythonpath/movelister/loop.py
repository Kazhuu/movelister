from movelister import messageBox


def getColumnLocation(sheet, columnName):
    x = -1
    column = -1

    # The loop iterates through the row 0 of chosen List to find where a certain Column is.
    while x < 80:
        x = x + 1
        if sheet.getCellByPosition(x, 0).getString() == columnName:
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


def getEndOfList(sheet):
    x = 1
    endRow = -1

    # The loop iterates through a list to figure out where it ends.
    # The loop breaks once there are two empty rows or x is over 1000.
    # Currently only used with Modifier List and Master List.
    # I'm sure there's a better way to programmatically reach the end of a list.
    while x < 1000:
        if sheet.getCellByPosition(0, x).getString() == '':
            if sheet.getCellByPosition(0, x + 1).getString() == '':
                        endRow = x - 1
                        break
        x = x + 1
    return endRow
