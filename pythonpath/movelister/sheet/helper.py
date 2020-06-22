from movelister.core.context import Context


def getActiveSheetName():
    """
    Return currently active sheet name.
    """
    document = Context.getDocument()
    activeSheet = document.getCurrentController().getActiveSheet()
    return activeSheet.getName()


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


def stripTrailingEmptyRows(data):
    """
    This code is used when instantiating certain classes and the code reads from sheet.
    """
    endIndex = len(data)
    for index, row in reversed(list(enumerate(data))):
        text = str(''.join(row))
        if text == '':
            endIndex = endIndex - 1
        else:
            break
    return data[:endIndex]


def normalizeArray(data):
    """
    Makes all lines of an array equally long to avoid pesky uno runtime errors.
    """
    highestLength = 0
    for line in data:
        if len(line) > highestLength:
            highestLength = len(line)
    for line in data:
        if len(line) < highestLength:
            difference = highestLength - len(line)
            line.extend(['' for i in range(difference)])
    return data
