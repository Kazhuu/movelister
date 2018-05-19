import uno
from com.sun.star.table import CellRangeAddress

from movelister import environment


def group_rows(sheet, start_row, nb_rows):
    cra = CellRangeAddress()
    cra.StartRow = start_row
    cra.EndRow = start_row + nb_rows
    # This sheet function requires CellRangeAddress + orientation.
    sheet.group(cra, 1)
    return None


def main(*args):
    # Basic things to connect to the document.
    desktop = environment.getDesktop()
    model = desktop.getCurrentComponent()
    sheet = model.CurrentController.ActiveSheet
    # Placeholder values.
    start_row = 10
    nb_rows = 10

    group_rows(sheet, start_row, nb_rows)


g_exportedScripts = (main,)
