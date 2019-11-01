import uno
from com.sun.star.beans import XPropertySet
from com.sun.star.beans import PropertyValue
from com.sun.star.sheet import XSheetConditionalEntries
from com.sun.star.sheet.ConditionOperator import NONE, EQUAL, NOT_EQUAL, GREATER, \
                                                 GREATER_EQUAL, LESS, LESS_EQUAL, BETWEEN, NOT_BETWEEN, FORMULA

from movelister.core import cursor
from movelister.format import convert


def applyConditionalFormatting(sheet, resultsDataArray, resultsListColors):

    # To do: finish this function. It does nothing so far.
    # info can be found here:
    # https://wiki.openoffice.org/wiki/Documentation/DevGuide/Spreadsheets/Conditional_Formats

    # Problems so far:
    # 1, it's not possible to clear existing conditional format entries by accessing
    #    through a specific range. However, this doesn't matter with the newest version
    #    where sheets are generated anew entirely each time.
    # 2, when trying to add a new condition to conForm (accessed via range), it says conversion
    #    not possible for some reason.
    # 3, a conForm (created as a XSheetConditionalEntries) doesn't seem to work at all
    #    like intended. It doesn't recognize the commands it should have.

    cra = cursor.getUsedAreaSize(sheet)
    range = convert.cellRangeAddressIntoCellRange(cra)

    conForm = range.ConditionalFormat

    # print(resultsDataArray)
    # print(resultsListColors)

    xPropSet = XPropertySet()
    # conForm = XSheetConditionalEntries()

    # condition = uno.createUnoStruct('com.sun.star.beans.PropertyValue')
    condition = PropertyValue()

    condition.Name = 'Operator'
    condition.Value = (LESS)

    # conForm.addNew(condition)


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
