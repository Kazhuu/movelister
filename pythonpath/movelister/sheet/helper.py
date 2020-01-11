def getActiveSheet(document):
    """
    This function gets the sheet that is currently active in the document.
    """
    activeSheet = document.getCurrentController().getActiveSheet()
    return activeSheet


def getHeaderRowPosition(sheetData):
    """
    This function figures out at what position the header row is. This may vary
    between sheets because of UI. The code is simple and basically looks for
    the first non-empty cell on second column.
    """
    for index, row in enumerate(sheetData):
        if row[1] != '':
            return index
    return 0


def getColumnPosition(sheetData, columnName):
    """
    This function iterates through the header row and return given column name
    index.
    """
    headerRow = getHeaderRowPosition(sheetData)
    columnRow = sheetData[headerRow]
    return columnRow.index(columnName)


def getRowPosition(sheetData, text, column):
    """
    This function iterates through a column to find the location of a cell that
    contains a chosen string.
    """
    for index, row in enumerate(sheetData):
        if row[column] == text:
            return index
    raise ValueError('{0} is not in column {1}'.format(text, column))


def getCellColorsFromColumn(sheet, column, top, bottom):
    """
    This function creates an array of CellBackColor values from given column
    and includes cells from top to bottom.
    """
    colors = []
    colorRange = sheet.getCellRangeByPosition(column, top, column, bottom)
    for index in range(0, bottom - top):
        colors.append(colorRange.getCellByPosition(0, index).CellBackColor)
    return colors


def createEmptyRow(length):
    """
    The purpose of this function is to generate an empty list that is as long as specified
    as well as compatible with cursor functions. Used in expanding existing data rows arrays.
    """
    emptyList = []

    for i in range(length):
        emptyList.append('')

    return emptyList
