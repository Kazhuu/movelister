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


def getColumnLength(sheet):
    """
    Get amount of columns in given sheet.
    """
    return getUsedAreaSize(sheet).EndColumn


def getSheetContent(sheet):
    """
    Returns two dimensional array of all non empty content of the given
    sheet. Array contains string and double values.
    """
    cursor = sheet.createCursor()
    cursor.gotoStartOfUsedArea(False)
    cursor.gotoEndOfUsedArea(True)
    return [list(row) for row in cursor.getDataArray()]


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


def getColumn(sheet, columnIndex):
    """
    Return column used content from given index as one-dimensional array.
    Data is just a slice of used sheet space returned by getSheetContent().
    So if used space is larger than sliced row content, then empty cells
    are included in with empty strings.
    """
    cursor = sheet.createCursor()
    cursor.gotoStartOfUsedArea(False)
    cursor.gotoEndOfUsedArea(True)
    rangeAddress = cursor.getRangeAddress()
    # left, top, right, bottom.
    data = cursor.getCellRangeByPosition(
        columnIndex, rangeAddress.StartRow, columnIndex, rangeAddress.EndRow).getDataArray()
    # Transfer two-dimensional array to one-dimensional array.
    return [i[0] for i in data]


def getColumns(sheet, startIndex, endIndex):
    """
    Slice data by columns from sheet used area starting from startIndex and
    including endIndex.
    """
    if startIndex > endIndex:
        raise IndexError('startIndex {0} cannot be bigger than endIndex {1}'.format(startIndex, endIndex))
    content = getSheetContent(sheet)
    if endIndex > len(content[0]):
        raise IndexError('endIndex {0} bigger than used area index {1}'.format(endIndex, len(content[0])))
    area = slice(startIndex, endIndex + 1)
    result = []
    for row in content:
        result.append(list(row[area]))
    return result


def getRow(sheet, rowIndex):
    """
    Return row used content from given index as one-dimensional array.
    Data is just a slice of used sheet space returned by getSheetContent().
    So if used space is larger than sliced row content, then empty cells
    are included in with empty strings.
    """
    cursor = sheet.createCursor()
    cursor.gotoStartOfUsedArea(False)
    cursor.gotoEndOfUsedArea(True)
    rangeAddress = cursor.getRangeAddress()
    # left, top, right, bottom.
    data = cursor.getCellRangeByPosition(
        rangeAddress.StartColumn, rowIndex, rangeAddress.EndColumn, rowIndex).getDataArray()
    # Transfer two-dimensional array to one-dimensional array.
    return list(data[0])
