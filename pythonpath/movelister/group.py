from com.sun.star.table import CellRangeAddress


def groupRows(sheet, startRow, endRow):
    cra = CellRangeAddress()
    cra.StartRow = startRow
    cra.EndRow = endRow
    sheet.group(cra, 1)
