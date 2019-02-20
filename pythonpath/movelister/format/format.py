from movelister.core import Alignment, cursor


def setHorizontalAlignmentToRange(sheet, alignment, startColumn, amount):
    """
    This function sets the horizontal alignment of columns in a given range
    to a chosen Alignment (enum).
    """
    area = cursor.getSheetContent(sheet)
    cellRange = sheet.getCellRangeByPosition(startColumn, 0, startColumn + amount, len(area) - 1)

    if alignment == Alignment.LEFT:
        cellRange.HoriJustify = 1
    elif alignment == Alignment.CENTER:
        cellRange.HoriJustify = 2
    elif alignment == Alignment.RIGHT:
        cellRange.HoriJustify = 3
    else:
        cellRange.HoriJustify = 0


def setOptimalWidthToRange(sheet, startColumn, amount):
    """
    This function sets the OptimalWidth of all columns in range to 1 (true).
    """
    cellRange = sheet.getCellRangeByPosition(startColumn, 0, startColumn + amount, 1)
    cellRange.getColumns().OptimalWidth = 1
