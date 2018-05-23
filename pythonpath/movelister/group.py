from com.sun.star.table import CellRangeAddress
from com.sun.star.table.TableOrientation import ROWS


def groupRows(sheet, groupStartRow, groupEndRow):
    cra = CellRangeAddress()
    cra.Sheet = sheet.RangeAddress.Sheet
    cra.StartRow = groupStartRow
    cra.EndRow = groupEndRow
    sheet.group(cra, ROWS)


def ungroupRows(sheet, groupStartRow, groupEndRow):
    cra = CellRangeAddress()
    cra.Sheet = sheet.RangeAddress.Sheet
    cra.StartRow = groupStartRow
    cra.EndRow = groupEndRow
    sheet.ungroup(cra, ROWS)
