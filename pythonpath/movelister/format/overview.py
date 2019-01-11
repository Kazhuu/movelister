from movelister.core import cursor
from movelister.sheet.sheet import Sheet


header_prefix = ['Action Name', 'Hit', 'Frames', 'Phase', 'DEF']
header_postfix = ['Notes 1', 'Notes 2', 'Notes 3']


class FormatOverview:

    def __init__(self, overview):
        self.instance = overview

    def generate(self):
        sheet = Sheet.newOverview(self.instance.name)
        cursor.setSheetContent(sheet, self.format)
        return sheet

    def format(self):
        data = []
        data.append(self.formatHeader())
        return data

    def formatHeader(self):
        modifiers = []
        for mod in self.instance.modifiers:
            modifiers.append(mod.name)
        return header_prefix + modifiers + header_postfix
