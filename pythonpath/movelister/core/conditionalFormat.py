import uno
from com.sun.star.beans import XPropertySet
from com.sun.star.beans import PropertyValue
from com.sun.star.sheet import XSheetConditionalEntries
from com.sun.star.sheet.ConditionOperator import NONE, EQUAL, NOT_EQUAL, GREATER, \
                                                 GREATER_EQUAL, LESS, LESS_EQUAL, BETWEEN, NOT_BETWEEN, FORMULA

from movelister.core import cursor
from movelister.format import convert


def applyConditionalFormatting(sheet, resultsDataArray, resultsListColors):

    # TODO: finish this function. It does nothing so far.
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
