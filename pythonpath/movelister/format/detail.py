from movelister.core import cursor
from movelister.sheet.sheet import Sheet


class DetailFormatter:
    """
    Class responsible for formatting Detail class instance to two
    dimensional array.

    TODO: write code.
    """

    def __init__(self, details):
        self.instance = details

    def generate(self):
        sheet = Sheet.newOverview(self.instance.name)
        cursor.setSheetContent(sheet, self.format())
        return sheet

    def format(self):
        data = []
        return data

    def _formatRow(self, phase):
        row = []
        return row
