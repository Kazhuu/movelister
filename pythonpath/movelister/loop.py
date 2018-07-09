from movelister import cursor, messageBox


def getColumnPosition(sheet, columnName):
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


def getRowPosition(sheet, column, string):
    columnRow = cursor.getColumn(sheet, column)
    rowPosition = -1

    # The loop iterates through the row 0 of chosen List to find where a certain Column is.
    x = -1
    while x < len(columnRow):
        x = x + 1
        if columnRow[x] == string:
            rowPosition = x
            break

    # Error message if it wasn't found.
    if column == - 1:
        messageBox.createMessage('OK', 'Warning:', "Program couldn't find a cell with " + string + '.')
        exit()

    return rowPosition


def turnArraySideways(array):
    '''
    This code turns a 2d-array so that its columns become rows and vice-versa.
    '''
    newList = []

    for item in array[0]:
        newList.append([])

    x = -1
    for row in array:
        x = x + 1
        y = - 1
        for item in row:
            y = y + 1
            newList[y].append(item)

    return newList
