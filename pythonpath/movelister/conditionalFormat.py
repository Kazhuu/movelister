from movelister import cursor

import uno
from com.sun.star.beans import PropertyValue
from com.sun.star.sheet.ConditionOperator import LESS


def applyConditionalFormatting(sheet, resultsDataArray, resultsListColors):

    # To do: finish this function. It does nothing so far.
    # range = sheet.getCellRangeByPosition(1, 1, 12, 12)
    # conForm = range.ConditionalFormat

    print(resultsDataArray)
    print(resultsListColors)

    condition = uno.createUnoStruct('com.sun.star.beans.PropertyValue')

    condition.Name = 'Operator'
    condition.Value = (LESS)

    # conForm.addNew(condition)

    # condition1 = PropertyValue()
    # condition1.value = 1

    # conForm.addNew(condition1)


def clearConditionalFormatting(sheet):

    # Test. Doesn't actually do what you'd expect it to do?
    range = sheet.getCellRangeByPosition(1, 1, 100, 100)
    range.ConditionalFormat.clear()

    print('Nothing here yet.')
    # To do: a function that deletes all existing Conditional Formatting in a sheet.

    # Explanation: making changes to a document usually fractures Conditional Formatting into many small ranges.
    # Having to deal with dozens or hundreds of small ranges slows down some LibreOffice functions a LOT.
    # Deleting all the ranges and then programmatically creating one intact big range is one way to optimize,
    # and it should probably be done after every large change in the file.
