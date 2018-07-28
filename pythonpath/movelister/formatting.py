def setOptimalWidthToRange(sheet, startCol, amount):
    """
    This function sets the OptimalWidth of all columns in range to 1 (true).
    """
    cellRange = sheet.getCellRangeByPosition(startCol, 0, startCol + amount, 1)
    cellRange.getColumns().OptimalWidth = 1
