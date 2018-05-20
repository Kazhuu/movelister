import uno
from com.sun.star.table import CellRangeAddress

import environment


def group_rows(sheet, startRow, nbRows):
    cra = CellRangeAddress()
    cra.StartRow = startRow
    cra.EndRow = startRow + nbRows
    # This sheet function requires CellRangeAddress + orientation.
    sheet.group(cra, 1)
    return None


def main(*args):
    # Basic things to connect to the document.
    desktop = environment.getDesktop()
    model = desktop.getCurrentComponent()
    sheet = model.CurrentController.ActiveSheet
    # Placeholder values.
    startRow = 10
    nbRows = 10

    group_rows(sheet, startRow, nbRows)


g_exportedScripts = (main,)
