from com.sun.star.beans import PropertyValue


def getResultsList(resultsSheet):
    x = 1
    resultsList = [0]

    # Iterate through Results List first column to get a list of Results.
    while x < 100:
        if resultsSheet.getCellByPosition(0, x).getString() != '':
            resultsList.append(resultsSheet.getCellByPosition(0, x).getString())
        elif resultsSheet.getCellByPosition(0, x + 1).getString() == '':
                break
        x = x + 1

    return resultsList


def getResultsListColors(resultsSheet, resultsList):
    x = 1
    resultsListColors = [0]

    # Iterate through Results List second column to get a list of colors.
    while x < len(resultsList):
        resultsListColors.append(resultsSheet.getCellByPosition(1, x).CellBackColor)
        x = x + 1

    return resultsListColors


def applyConditionalFormatting(sheet, resultsList, resultsListColors):

    # Just a test.
    range = sheet.getCellRangeByPosition(1, 2, 11, 12)
    conForm = range.ConditionalFormat

    print(resultsList)
    print(resultsListColors)

    # condition1 = PropertyValue()
    # condition1.value = 1

    # conForm.addNew(condition1)

    print('hello')
    # cra = CellRangeAddress()
    # cra.StartRow = startRow
    # cra.EndRow = endRow
    # sheet.group(cra, 1)
