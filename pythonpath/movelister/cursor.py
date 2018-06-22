def getUsedAreaSize(sheet):
    """
    Returns used sheet area as a CellRangeAddress object.
    See http://www.openoffice.org/api/docs/common/ref/com/sun/star/table/CellRangeAddress.html
    for object methods.
    """
    cursor = sheet.createCursor()
    cursor.gotoStartOfUsedArea(False)
    cursor.gotoEndOfUsedArea(True)
    return cursor.getRangeAddress()


def getSheetContent(sheet):
    """
    Returns two dimensional array of all non empty content of the given
    sheet. Array contains string and double values.
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


def getRowsContent(sheet, startRow, endRow):
    """
    Return given rows data in two dimensional array. Data is just a
    slice of used sheet space returned by getSheetContent(). So if
    used space is larger than sliced row content, then empty cells
    are included in with empty strings.
    """
    cursor = sheet.createCursor()
    cursor.gotoStartOfUsedArea(False)
    cursor.gotoEndOfUsedArea(True)
    rangeAddress = cursor.getRangeAddress()
    # left, top, right, bottom
    return cursor.getCellRangeByPosition(startRow, rangeAddress.StartRow, endRow, rangeAddress.EndRow).getDataArray()
