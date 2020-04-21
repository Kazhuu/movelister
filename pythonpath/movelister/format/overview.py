from movelister.core import cursor
from movelister.format import color
from movelister.model.modifier import Modifier
from movelister.sheet.modifiers import Modifiers
from movelister.sheet.overview import Overview
from movelister.sheet.sheet import Sheet
from movelister.format.action import ActionFormatter


headerPrefix = ['Action Name', 'Hit', 'Frames', 'Phase', 'DEF']
headerPostfix = ['Notes 1', 'Notes 2', 'Notes 3']


class OverviewFormatter:
    """
    Class responsible for formatting Overview class instance into a two dimensional
    array.
    """

    def __init__(self, overview):
        self.instance = overview

    def generate(self):
        """
        Generate new Overview sheet by copying template sheet and placing
        formatted Overview class instance data in it.
        """
        sheet = Sheet.newOverview(self.instance.name)
        cursor.setSheetContent(sheet, self.format())
        return sheet

    def format(self):
        """
        Format whole Overview and returns two dimensional data array which
        can be put to sheet. It also includes empty row before header row.
        """
        data = []
        data.append(self.formatFirstLine())
        data.append(self.formatHeader())
        data = data + self.formatActions()
        return data

    def formatHeader(self):
        """
        Format Overview header information with modifier data in it and
        return it as an array.
        """
        modifiers = []
        for mod in self.instance.modifiers:
            modifiers.append(mod.name)
        return headerPrefix + modifiers + headerPostfix

    def formatActions(self):
        """
        Format actions and return it as two dimensional array.
        """
        rows = []
        for action in self.instance.actions:
            rows = rows + ActionFormatter(self.instance, action, len(headerPostfix)).format()
        return rows

    def formatFirstLine(self):
        """
        Return the empty row before actual header row. In the template this row contains the buttons.
        """
        length = len(headerPrefix) + len(headerPostfix) + len(self.instance.modifiers)
        return ['' for _ in range(0, length)]

    def setOverviewModifierColors(self, sheetName):
        """
        This function sets colors to all the columns in the modifier block of an Overview.
        """
        overview = Overview.fromSheet(sheetName)
        modifiers = Modifiers('Modifiers')
        columnLength = len(overview.data)
        startCol = overview.modifierStartColumn
        headerRow = overview.headerRowIndex

        offset = 0
        for a in range(len(overview.modifiers)):
            currentColor = color.Color(modifiers.modifierColors[a])
            nextColor = color.Color(0)

            # Ensures that no runtime error is created from reading from a too high index.
            if a != len(overview.modifiers) - 1:
                nextColor = color.Color(modifiers.modifierColors[a + 1])

            # Compares the color value of the current and next column. If they're the same
            # then they can be colored in the same CellRange to save time.
            if currentColor.value == nextColor.value:
                offset = offset + 1
            else:
                overview.sheet.getCellRangeByPosition(
                    startCol + a - offset, headerRow, startCol + a, columnLength - headerRow
                    ).CellBackColor = currentColor.value
                offset = 0

    def setOverviewActionColors(self, sheetName):
        """
        This function sets colors to all the actions in the action column on an Overview.

        TO DO: seems to be in progress.
        """
        overview = Overview.fromSheet(sheetName)
        print()
