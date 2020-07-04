from movelister.core import cursor, names
from movelister.format.detail import DetailFormatter
from movelister.sheet import helper
from movelister.sheet.sheet import Sheet


headerPrefix = ['Action Name', 'Modifiers', 'Input to Compare']
headerPostfix = ['Notes 1', 'Notes 2', 'Notes 3']


class DetailsFormatter:
    """
    Class responsible for formatting Details class instance into a two dimensional
    array.
    """

    def __init__(self, details, overview):
        self.instance = details
        # Modifier names are used for sorting.
        self.modifierNames = overview.modifierNames()
        self.maximumPhases = overview.highestPhase
        self.parentOverviewName = names.getOverviewName(self.instance.viewName)

    def generate(self):
        """
        Generate new Details sheet by copying template sheet and placing
        formatted Details class instance data in it.
        """
        sheet = Sheet.newDetails(self.parentOverviewName, self.instance.name)
        cursor.setSheetContent(sheet, self.format())
        return sheet

    def format(self):
        """
        Format whole Details and returns two dimensional data array which
        can be put to sheet.
        """
        data = []
        data.append(self.formatHeader())
        data.extend(self.formatDetails())
        return helper.normalizeArray(data)

    def formatHeader(self):
        """
        Formats the header row of the Details-sheet. Wideness of the row varies depending on
        the maximum amount of phases in an action, as specified in Overview.
        """
        data = []
        for a in headerPrefix:
            data.append(a)
        for a in range(self.maximumPhases):
            data.append('')
            data.append('> Phase ' + str(a) + ' result')
            data.append('')
        for a in headerPostfix:
            data.append(a)
        return data

    def formatDetails(self):
        """
        Format details and return them as two dimensional array.
        """
        rows = []
        for detail in self.instance.details:
            rows.extend(DetailFormatter(detail, self.modifierNames).format() + [['']])
        return rows
