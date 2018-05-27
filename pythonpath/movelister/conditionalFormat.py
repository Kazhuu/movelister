import uno
from com.sun.star.beans import PropertyValue
from com.sun.star.sheet.ConditionOperator import LESS


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


def getResultsListColors(resultsSheet, listLength):
    x = 1
    resultsListColors = [0]

    # Iterate through Results List second column to get a list of colors.
    while x < listLength + 1:
        resultsListColors.append(resultsSheet.getCellByPosition(1, x).CellBackColor)
        x = x + 1

    return resultsListColors


def applyConditionalFormatting(sheet, resultsList, resultsListColors):

    # Just a test.
    range = sheet.getCellRangeByPosition(1, 1, 12, 12)
    conForm = range.ConditionalFormat

    print(resultsList)
    print(resultsListColors)

    condition = uno.createUnoStruct("com.sun.star.beans.PropertyValue")

    condition.Name = "Operator"
    condition.Value = (LESS)

    # conForm.addNew(condition)

    # condition1 = PropertyValue()
    # condition1.value = 1

    # conForm.addNew(condition1)
