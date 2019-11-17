import string
from movelister.core import Context


def cellRangeAddressIntoCellRange(cra):
    """
    This code converts a Cell Range Address into a more useable Cell Range object.
    """
    model = Context.getDocument()
    sheet = model.Sheets.getByIndex(cra.Sheet)
    range = sheet.getCellRangeByPosition(cra.StartColumn, cra.StartRow, cra.EndColumn, cra.EndRow)
    return range


def convertIntoBaseAddress(num):
    """
    This code converts column number into base address (Base 26) since some LibreOffice features need it.
    """
    chars = []
    while num > 0:
        num, d = divmodFunction(num)
        chars.append(string.ascii_uppercase[d - 1])
    return ''.join(reversed(chars))


def divmodFunction(n):
    a, b = divmod(n, 26)
    if b == 0:
        return a - 1, b + 26
    return a, b


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
