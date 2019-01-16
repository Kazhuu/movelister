from movelister.core import cursor
from movelister.sheet.sheet import Sheet
from .modified_action import ModifiedActionFormatter


header_prefix = ['Action Name', 'Hit', 'Frames', 'Phase', 'DEF']
header_postfix = ['Notes 1', 'Notes 2', 'Notes 3']


class OverviewFormatter:
    """
    Class responsible formatting Overview class instance to two dimensional
    array.
    """

    def __init__(self, overview):
        self.instance = overview

    def generate(self):
        """
        Generate new overview sheet by copying template sheet and placing
        formatted Overview class instance data in it.
        """
        sheet = Sheet.newOverview(self.instance.name)
        cursor.setSheetContent(sheet, self.format())
        return sheet

    def format(self):
        """
        Format whole overview and returns two dimensional data array which
        can be put to sheet. It also includes empty row before header row.
        """
        data = []
        data.append(self.formatFirstLine())
        data.append(self.formatHeader())
        data = data + self.formatModifiedActions()
        return data

    def formatHeader(self):
        """
        Format overview header information with modifier data in it and
        returns it as an array.
        """
        modifiers = []
        for mod in self.instance.modifiers:
            modifiers.append(mod.name)
        return header_prefix + modifiers + header_postfix

    def formatModifiedActions(self):
        """
        Format modified actions and returns it as two dimensional array.
        """
        rows = []
        for modifiedAction in self.instance.modifiedActions:
            rows = rows + ModifiedActionFormatter(self.instance, modifiedAction, len(header_postfix)).format()
        return rows

    def formatFirstLine(self):
        """
        Returns empty row before actual header row. In template this includes buttons.
        """
        length = len(header_prefix) + len(header_postfix) + len(self.instance.modifiers)
        return ['' for _ in range(0, length)]