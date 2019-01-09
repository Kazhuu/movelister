from movelister.core import cursor
from movelister.sheet import Sheet


class FormatOverview:

    def __init__(self, overview):
        self.instance = overview

    def generate(self):
        sheet = Sheet.newOverview(self.instance.name)
        cursor.setSheetContent(sheet, self.format)
        return sheet

    def _format(self):
        return None
