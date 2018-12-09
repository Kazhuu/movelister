from movelister import color
from movelister.core import cursor
from movelister.sheet import helper


def getTitleBarColor(optionsSheet):
    """
    This function gets the value of the cell background color from the Options-section.
    """
    titleBarRow = helper.getRowPosition(optionsSheet, 'Title Bar Color:', 0)

    c = color.Color(optionsSheet.getCellByPosition(1, titleBarRow).CellBackColor)
    return c


def setTitleBarColor(sheet, optionsSheet, rowAmount):
    """
    This function sets the cell background color of the top rows of a sheet to a chosen value.
    The amount of rows can be customized because of UI, which may change the height of title bar in some sheets.
    """
    row = cursor.getRow(sheet, 0)

    color = getTitleBarColor(optionsSheet)
    cellRange = sheet.getCellRangeByPosition(0, 0, len(row) - 1, 0 + rowAmount)
    cellRange.CellBackColor = color.value


def setOverviewModifierColors(overviewSheet, startCol, endCol, modifierListColors):
    """
    This function sets colors to all the individual columns in the modifier block of an Overview.
    """
    offset = 0
    tempCol = cursor.getColumn(overviewSheet, startCol)
    modifierListColors.append(0)

    headerRowPosition = helper.getHeaderRowPosition(overviewSheet)

    x = -1
    for a in range(len(modifierListColors) - 1):
        x = x + 1
        currentColor = color.Color(modifierListColors[x])
        nextColor = color.Color(modifierListColors[x + 1])

        if currentColor.value == nextColor.value:
            offset = offset + 1
        else:
            overviewSheet.getCellRangeByPosition(startCol + x - offset, headerRowPosition, startCol + x,
                                                 len(tempCol) - headerRowPosition).CellBackColor = currentColor.value
            offset = 0


def setDetailsSheetColors(detailsSheet, actionColors, modifierColors, inputColors):
    print('TO DO')


def setHorizontalAlignmentToSheet(sheet, alignment):
    """
    This function sets the horizontal alignment of a sheet to a chosen value.
    """
    area = cursor.getSheetContent(sheet)
    cellRange = sheet.getCellRangeByPosition(0, 0, len(area[0]) - 1, len(area) - 1)

    if alignment == 'LEFT':
        cellRange.HoriJustify = 1
    elif alignment == 'CENTER':
        cellRange.HoriJustify = 2
    elif alignment == 'RIGHT':
        cellRange.HoriJustify = 3
    else:
        cellRange.HoriJustify = 0


def setOptimalWidthToRange(sheet, startCol, amount):
    """
    This function sets the OptimalWidth of all columns in range to 1 (true).
    """
    cellRange = sheet.getCellRangeByPosition(startCol, 0, startCol + amount, 1)
    cellRange.getColumns().OptimalWidth = 1
