
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
        print()
        # sheet = Sheet.newOverview(self.instance.name)
        # cursor.setSheetContent(sheet, self.format())
        # return sheet

    def format(self):
        """
        Format whole Details and returns two dimensional data array which
        can be put to sheet.
        """
        data = []
        return data
