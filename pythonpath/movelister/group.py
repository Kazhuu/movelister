from com.sun.star.table import CellRangeAddress


def groupRows(sheet, groupStartRow, groupEndRow):
    cra = CellRangeAddress()
    cra.Sheet = sheet.RangeAddress.Sheet
    cra.StartRow = groupStartRow
    cra.EndRow = groupEndRow
    sheet.group(cra, 1)


def ungroupRows(sheet, groupStartRow, groupEndRow):
    cra = CellRangeAddress()
    cra.Sheet = sheet.RangeAddress.Sheet
    cra.StartRow = groupStartRow
    cra.EndRow = groupEndRow
    sheet.ungroup(cra, 1)
