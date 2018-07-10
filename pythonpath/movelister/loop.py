from movelister import cursor, loop, messageBox


def getColumnPosition(sheet, columnName):
    """
    This function iterates through the row 0 of chosen List to find where a certain Column is.
    """
    columnRow = cursor.getRow(sheet, 0)
    column = -1

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


def getColorArray(sheet):
    """
    This function creates an array of CellBackColor from the Color column in a chosen sheet.
    The loop starts counting from 0 and thus skips the top row with labels on it.
    """
    sheetLength = cursor.getColumn(sheet, 0)
    colPosition = loop.getColumnPosition(sheet, 'Color')
    colorList = []

    x = 0
    while x < len(sheetLength) - 1:
        x = x + 1
        colorList.append(sheet.getCellByPosition(colPosition, x).CellBackColor)

    return colorList


def turnArraySideways(array):
    """
    This code turns a 2d-array so that its columns become rows and vice-versa.
    """
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
