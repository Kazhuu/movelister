from movelister import loop


def getResultsList(resultsSheet):
    endRow = -1

    # The loop iterates through Master Action List to get its end row.
    # The loop breaks once there are two empty rows or x is over 1000.
    endRow = loop.getEndOfList(resultsSheet)

    # The four attributes for CellRangeByPosition are: left, top, right, bottom.
    # To do: the wideness of this array isn't well defined yet. It depends on
    # what's all the data that's actually needed elsewhere.
    range = resultsSheet.getCellRangeByPosition(0, 1, 0, endRow)

    resultsDataArray = range.getDataArray()
    return resultsDataArray


def getResultsListColors(resultsSheet, listLength):
    x = 1
    resultsListColors = [0]

    # Iterate through Results List second column to get a list of colors.
    while x < listLength + 1:
        resultsListColors.append(resultsSheet.getCellByPosition(1, x).CellBackColor)
        x = x + 1

    return resultsListColors
