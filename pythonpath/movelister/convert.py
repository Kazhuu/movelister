from movelister.context import Context


def cellRangeAddressIntoCellRange(cra):
    """
    This code converts a Cell Range Address into a more useable Cell Range object.
    """
    model = Context.getDocument()
    sheet = model.Sheets.getByIndex(cra.Sheet)
    range = sheet.getCellRangeByPosition(cra.StartColumn, cra.StartRow, cra.EndColumn, cra.EndRow)
    return range


def convertIntoNestedTuple(list):
    """
    This code converts an 1d List into a 2d Tuple that is compatible with a data array of a sheet.
    """
    tempTuple = tuple(list)
    tempList = [[]]
    tempList[0] = tempTuple
    tempTuple2 = tuple(tempList)

    return tempTuple2


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
