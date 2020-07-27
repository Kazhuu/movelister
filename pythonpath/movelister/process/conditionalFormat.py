from com.sun.star.beans import PropertyValue
from com.sun.star.sheet.ConditionOperator import EQUAL

from movelister.core import cursor


def createDetailsConditionalFormats(detailsUnoSheet, masterSheet, resultsSheet, inputsSheet):
    """
    Create conditional formats for the given details sheet. Three conditional
    format areas are created. One for action names, one for input names and one
    largest one for results of different phases.
    """
    createResultsConditionalFormat(detailsUnoSheet, resultsSheet)
    createInputsConditionalFormat(detailsUnoSheet, inputsSheet)
    createActionConditionalFormats(detailsUnoSheet, masterSheet)


def createResultsConditionalFormat(detailsUnoSheet, resultsSheet):
    """
    Create one large conditional format area which covers all phases result
    columns. This conditional format is used to apply background color from
    Results sheet.
    """
    width, heigth = cursor.getWidthAndHeight(detailsUnoSheet)
    resultStyleNames = resultsSheet.getResultStyleNames()
    resultRange = detailsUnoSheet.getCellRangeByPosition(3, 1, width, heigth)
    resultsConditionalFormat = resultRange.ConditionalFormat
    return _createConditionalFormat(resultRange, resultStyleNames)


def createInputsConditionalFormat(detailsUnoSheet, inputsSheet):
    """
    Create conditional format to input column which applies background color
    from Inputs sheet for different input names.
    """
    inputColumn = 2
    rowCount = cursor.getHeight(detailsUnoSheet)
    inputStyleNames = inputsSheet.getInputStylesNames()
    inputRange = detailsUnoSheet.getCellRangeByPosition(inputColumn, 1, inputColumn, rowCount)
    inputConditionalFormat = inputRange.ConditionalFormat
    return _createConditionalFormat(inputRange, inputStyleNames)


def createActionConditionalFormats(detailsUnoSheet, masterSheet):
    """
    Create conditional format for action column which applies background color
    from Master List sheet for different action names.
    """
    actionColumn = 0
    rowCount = cursor.getHeight(detailsUnoSheet)
    actionStyleNames = masterSheet.getActionStyleNames()
    actionRange = detailsUnoSheet.getCellRangeByPosition(actionColumn, 1, actionColumn, rowCount)
    actionConditionalFormat = actionRange.ConditionalFormat
    return _createConditionalFormat(actionRange, actionStyleNames)


def _createConditionalFormat(cellRange, styleNamesPairs):
    """
    Create conditional format itself with needed properties. This is used as
    guide how this was done:
    https://wiki.openoffice.org/wiki/Documentation/DevGuide/Spreadsheets/Conditional_Formats
    """
    conditionalFormat = cellRange.ConditionalFormat
    for cellContent, styleName in styleNamesPairs:
        condition = PropertyValue()
        condition.Name = 'Operator'
        condition.Value = EQUAL
        formula = PropertyValue()
        formula.Name = 'Formula1'
        formula.Value = '"{0}"'.format(cellContent)
        style = PropertyValue()
        style.Name = 'StyleName'
        style.Value = styleName
        properties = [condition, formula, style]
        conditionalFormat.addNew(properties)
    cellRange.ConditionalFormat = conditionalFormat
    return cellRange.ConditionalFormat
