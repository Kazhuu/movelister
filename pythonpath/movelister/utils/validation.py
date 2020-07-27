import re
from movelister.core import cursor
from movelister.sheet.about import About
from movelister.sheet.sheet import ABOUT_SHEET_NAME


def setDataValidationToColumn(sheet, column, lastRow, name, type):
    """
    This code sets a specific type of data validation to a single column.

    ValidationType ENUM = (0) ANY, (1) WHOLE, (2) DECIMAL, (3) DATE, (4) TIME, (5) TEXT_LEN, (6) LIST, (7) CUSTOM
    ValidationAlertStyle ENUM = (0) STOP, (1) WARNING, (2) INFO, (3) MACRO
    ConditionOperator ENUM = (0) NONE, (1) EQUAL, (2) NOT_EQUAL, (3) GREATER, (4) GREATER_EQUAL, (5) LESS
                             (6) LESS_EQUAL, (7) BETWEEN, (8) NOT_BETWEEN, (9) FORMULA
    """

    range = sheet.getCellRangeByPosition(column, 1, column, lastRow)
    validation = range.Validation

    # Get relevant options from the About-screen.
    about = About(ABOUT_SHEET_NAME)
    showEntriesAscendingOption = about.isShowEntriesAscendingOn()

    if type == "phase":
        validation.Type = 2
        validation.ErrorAlertStyle = 0
        validation.setOperator(7)
        validation.ErrorMessage = "Please enter an integer between 0 and 99."
        validation.ShowErrorMessage = True
        validation.setFormula1(0.0)
        validation.setFormula2(99.0)

    if type == 'disable':
        validation.Type = 5
        validation.ErrorAlertStyle = 0
        validation.setOperator(1)
        validation.ErrorMessage = 'The content of this column is generated automatically. ' + \
                                  'Please don\'t modify it manually.'
        validation.ShowErrorMessage = True
        validation.setFormula1(0.0)

    if type == 'details-reaction':
        validation.Type = 6
        validation.ErrorAlertStyle = 0
        validation.setOperator(1)
        validation.setFormula1('$Results.$A$2:$Results.$A$50')

    if type == 'details-result':
        validation.Type = 6
        validation.ErrorAlertStyle = 0
        if showEntriesAscendingOption == True:
            validation.ShowList = 2
        validation.setOperator(1)
        validation.setFormula1('$\'Overview (' + name + ')\'.$A$3:$A$' + str(lastRow))

    if type == 'details-modifier':
        validation.Type = 6
        validation.ErrorAlertStyle = 0
        if showEntriesAscendingOption == True:
            validation.ShowList = 2
        validation.setOperator(1)
        validation.setFormula1('$B$2:$B$' + str(lastRow))

    range.Validation = validation


def setDataValidationToDetailsSheet(sheet, name):
    """
    This function sets data validation to all the Phase-columns in a Details-sheet.
    """
    colNum, lastRow = cursor.getWidthAndHeight(sheet)

    # Prevent code from crashing if sheet is empty.
    if lastRow == 0:
        lastRow = 10

    valType = 0
    for a in range(colNum):
        # Once column number gets high enough, break out of loop.
        if a > colNum - 3:
            break
        # Set a correct type of validation for each column. There are three relevant types
        # that repeat once for each Phase.
        if a > 2:
            if valType == 0:
                setDataValidationToColumn(sheet, a, lastRow, name, 'details-reaction')
            if valType == 1:
                setDataValidationToColumn(sheet, a, lastRow, name, 'details-result')
            if valType == 2:
                setDataValidationToColumn(sheet, a, lastRow, name, 'details-modifier')
            valType = valType + 1
            # Make sure validation type loops back to 0 for next Phase.
            if valType > 2:
                valType = 0
