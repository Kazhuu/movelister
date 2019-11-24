from movelister.core import HorizontalAlignment, VerticalAlignment, cursor


def setHorizontalAlignmentToRange(sheet, alignment, startColumn, amount):
    """
    This function sets the horizontal alignment of columns in a given range
    to a chosen HorizontalAlignment (enum).
    """
    area = cursor.getSheetContent(sheet)
    cellRange = sheet.getCellRangeByPosition(startColumn, 0, startColumn + amount, len(area) - 1)

    if alignment == HorizontalAlignment.LEFT:
        cellRange.HoriJustify = 1
    elif alignment == HorizontalAlignment.CENTER:
        cellRange.HoriJustify = 2
    elif alignment == HorizontalAlignment.RIGHT:
        cellRange.HoriJustify = 3
    else:
        cellRange.HoriJustify = 0


def setVerticalAlignmentToRange(sheet, alignment, startCol, startRow, endCol, endRow):
    """
    This function sets the vertical alignment of an area to a chosen
    VerticalAlignment (enum).
    """
    cellRange = sheet.getCellRangeByPosition(startCol, startRow, endCol, endRow)

    if alignment == VerticalAlignment.TOP:
        cellRange.VertJustify = 1
    elif alignment == VerticalAlignment.CENTER:
        cellRange.VertJustify = 2
    elif alignment == VerticalAlignment.BOTTOM:
        cellRange.VertJustify = 3
    else:
        cellRange.VertJustify = 0


def setOptimalWidthToRange(sheet, startColumn, amount):
    """
    This function sets the OptimalWidth of all columns in range to 1 (true).
    """
    cellRange = sheet.getCellRangeByPosition(startColumn, 0, startColumn + amount, 1)
    cellRange.getColumns().OptimalWidth = 1
