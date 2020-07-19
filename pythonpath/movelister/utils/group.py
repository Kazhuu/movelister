from com.sun.star.table import CellRangeAddress
from com.sun.star.table.TableOrientation import ROWS
from com.sun.star.table.TableOrientation import COLUMNS


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


def groupColumns(sheet, groupStartColumn, groupEndColumn):
    cra = CellRangeAddress()
    cra.Sheet = sheet.RangeAddress.Sheet
    cra.StartColumn = groupStartColumn
    cra.EndColumn = groupEndColumn
    sheet.group(cra, COLUMNS)


def ungroupColumns(sheet, groupStartColumn, groupEndColumn):
    cra = CellRangeAddress()
    cra.Sheet = sheet.RangeAddress.Sheet
    cra.StartColumn = groupStartColumn
    cra.EndColumn = groupEndColumn
    sheet.ungroup(cra, COLUMNS)
