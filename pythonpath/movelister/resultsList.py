from movelister import cursor


def getResultsList(resultsSheet):
    resultsDataArray = cursor.getSheetContent(resultsSheet)

    return resultsDataArray


def getResultsListColors(resultsSheet, listLength):
    x = 1
    resultsListColors = [0]

    # Iterate through Results List second column to get a list of colors.
    while x < listLength + 1:
        resultsListColors.append(resultsSheet.getCellByPosition(1, x).CellBackColor)
        x = x + 1

    return resultsListColors
