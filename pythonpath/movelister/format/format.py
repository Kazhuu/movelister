from com.sun.star.table.CellHoriJustify import STANDARD as HORIZONTAL_STANDARD
from com.sun.star.table.CellHoriJustify import LEFT as HORIZONTAL_LEFT
from com.sun.star.table.CellHoriJustify import CENTER as HORIZONTAL_CENTER
from com.sun.star.table.CellHoriJustify import RIGHT as HORIZONTAL_RIGHT
# For some reason UNO api has two enums CellVertJustify and CellVertJustify2
# for vertical alignment and from which latter one is the correct one.
from com.sun.star.table.CellVertJustify2 import STANDARD as VERTICAL_STANDARD
from com.sun.star.table.CellVertJustify2 import TOP as VERTICAL_TOP
from com.sun.star.table.CellVertJustify2 import CENTER as VERTICAL_CENTER
from com.sun.star.table.CellVertJustify2 import BOTTOM as VERTICAL_BOTTOM

from movelister.core import cursor
from movelister.core.alignment import HorizontalAlignment, VerticalAlignment


def setHorizontalAlignmentToRange(sheet, alignment, startColumn, amount):
    """
    This function sets the horizontal alignment of columns in a given range
    to a chosen HorizontalAlignment (enum).
    """
    area = cursor.getSheetContent(sheet)
    cellRange = sheet.getCellRangeByPosition(startColumn, 0, startColumn + amount, len(area) - 1)

    if alignment == HorizontalAlignment.LEFT:
        cellRange.HoriJustify = HORIZONTAL_STANDARD
    elif alignment == HorizontalAlignment.CENTER:
        cellRange.HoriJustify = HORIZONTAL_CENTER
    elif alignment == HorizontalAlignment.RIGHT:
        cellRange.HoriJustify = HORIZONTAL_RIGHT
    else:
        cellRange.HoriJustify = HORIZONTAL_STANDARD


def setVerticalAlignmentToRange(sheet, alignment, startCol, startRow, endCol, endRow):
    """
    This function sets the vertical alignment of an area to a chosen
    VerticalAlignment (enum).
    """
    cellRange = sheet.getCellRangeByPosition(startCol, startRow, endCol, endRow)

    if alignment == VerticalAlignment.TOP:
        cellRange.VertJustify = VERTICAL_TOP
    elif alignment == VerticalAlignment.CENTER:
        cellRange.VertJustify = VERTICAL_CENTER
    elif alignment == VerticalAlignment.BOTTOM:
        cellRange.VertJustify = VERTICAL_BOTTOM
    else:
        cellRange.VertJustify = VERTICAL_STANDARD


def setOptimalWidthToRange(sheet, startColumn, amount):
    """
    This function sets the OptimalWidth of all columns in range to 1 (true).
    """
    cellRange = sheet.getCellRangeByPosition(startColumn, 0, startColumn + amount, 1)
    cellRange.getColumns().OptimalWidth = 1
