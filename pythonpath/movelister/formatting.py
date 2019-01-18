from movelister.core import cursor
from movelister.model import color
from movelister.sheet import helper


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
