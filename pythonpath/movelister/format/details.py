from movelister.core import cursor
from movelister.format.detail import DetailFormatter
from movelister.sheet.sheet import Sheet


class DetailsFormatter:
    """
    Class responsible for formatting Details class instance into a two dimensional
    array.
    """

    def __init__(self, details):
        self.instance = details

    def generate(self):
        """
        Generate new Details sheet by copying template sheet and placing
        formatted Details class instance data in it.
        """
        sheet = Sheet.newDetails(self.instance.name)
        cursor.setSheetContent(sheet, self.format())
        return sheet

    def format(self):
        """
        Format whole Details and returns two dimensional data array which
        can be put to sheet.
        """
        data = []
        data = data + self.formatDetails()
        return data

    def formatDetails(self):
        """
        Format actions and return it as two dimensional array.
        """
        rows = []
        for detail in self.instance.actions:
            rows = rows + DetailFormatter(self.instance, detail).format()
        return rows
