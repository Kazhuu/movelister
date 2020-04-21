from com.sun.star.table.CellHoriJustify import STANDARD, LEFT, CENTER, RIGHT
import com.sun.star.table.CellVertJustify

from movelister.core import HorizontalAlignment, VerticalAlignment, cursor


def setHorizontalAlignmentToRange(sheet, alignment, startColumn, amount):
    """
    This function sets the horizontal alignment of columns in a given range
    to a chosen HorizontalAlignment (enum).
    """
    area = cursor.getSheetContent(sheet)
    cellRange = sheet.getCellRangeByPosition(startColumn, 0, startColumn + amount, len(area) - 1)

    if alignment == HorizontalAlignment.LEFT:
        cellRange.HoriJustify = LEFT
    elif alignment == HorizontalAlignment.CENTER:
        cellRange.HoriJustify = CENTER
    elif alignment == HorizontalAlignment.RIGHT:
        cellRange.HoriJustify = RIGHT
    else:
        cellRange.HoriJustify = STANDARD


def setVerticalAlignmentToRange(sheet, alignment, startCol, startRow, endCol, endRow):
    """
    This function sets the vertical alignment of an area to a chosen
    VerticalAlignment (enum).
    """
    cellRange = sheet.getCellRangeByPosition(startCol, startRow, endCol, endRow)

    if alignment == VerticalAlignment.TOP:
        cellRange.VertJustify = CellVertJustify.TOP
    elif alignment == VerticalAlignment.CENTER:
        cellRange.VertJustify = CellVertJustify.CENTER
    elif alignment == VerticalAlignment.BOTTOM:
        cellRange.VertJustify = CellVertJustify.BOTTOM
    else:
        cellRange.VertJustify = CellVertJustify.STANDARD


def setOptimalWidthToRange(sheet, startColumn, amount):
    """
    This function sets the OptimalWidth of all columns in range to 1 (true).
    """
    cellRange = sheet.getCellRangeByPosition(startColumn, 0, startColumn + amount, 1)
    cellRange.getColumns().OptimalWidth = 1
