import uno
from com.sun.star.table import CellRangeAddress


def main(*args):
    # basic things to connect to the document
    desktop = XSCRIPTCONTEXT.getDesktop()
    model = desktop.getCurrentComponent()
    sheet = model.CurrentController.ActiveSheet
    # placeholder values
    start_row = 10
    nb_rows = 10
    group_rows(sheet, start_row, nb_rows)


def group_rows(sheet, start_row, nb_rows):
    cra = CellRangeAddress()
    cra.StartRow = start_row
    cra.EndRow = start_row + nb_rows
    # this sheet function requires CellRangeAddress + orientation
    sheet.group(cra, 1)
    return None
