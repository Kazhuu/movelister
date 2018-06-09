def getSheetContent(sheet):
    """
    Returns two dimensional array of all non empty content of the given
    sheet. Array contais string and double values.
    """
    cursor = sheet.createCursor()
    cursor.gotoStartOfUsedArea(False)
    cursor.gotoEndOfUsedArea(True)
    return cursor.getDataArray()


def setSheetContent(sheet, data):
    """
    Overwrite entire data in given sheet with given data. Data must be a
    two dimensional array only containing string and doubles. An empty
    cell is given with empty string.
    """
    columns = len(data[0])
    rows = len(data)
    cursor = sheet.createCursor()
    cursor.gotoOffset(0, 0)
    cursor.collapseToSize(columns, rows)
    cursor.setDataArray(data)
