from movelister.core import cursor
from movelister.model import Color
from movelister.sheet import helper


def getTitleBarColor(aboutSheet):
    """
    This function gets the CellBackColor value of the Title Bar cell from the Options-section.
    """
    sheetContent = cursor.getSheetContent(aboutSheet)
    titleBarRow = helper.getRowPosition(sheetContent, 'Title Bar Color:', 0)

    c = Color(aboutSheet.getCellByPosition(1, titleBarRow).CellBackColor)
    return c


def setColorToRange(color, range):
    """
    This function just sets CellBackColor of a chosen CellRange.
    """
    range.CellBackColor = color.value
