def deleteRows(sheet, startRow, amount):
    sheet.Rows.removeByIndex(startRow, amount)


def deleteColumns(sheet, startColumn, amount):
    sheet.Columns.removeByIndex(startColumn, amount)
