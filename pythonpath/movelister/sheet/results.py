from movelister.core import cursor, styles
from movelister.sheet.sheet import Sheet
from movelister.sheet import helper

class Results:

    def __init__(self, sheetName):
        self.name = sheetName
        self.sheet = Sheet.getByName(sheetName)
        self.data = cursor.getSheetContent(self.sheet)
        self.headerRowIndex = helper.getHeaderRowPosition(self.data)
        self.dataBeginRow = self.headerRowIndex + 1
        self.resultColumnIndex = helper.getColumnPosition(self.data, 'Results', 0)
        self.colorColumnIndex = helper.getColumnPosition(self.data, 'Color', 1)
        self.dataRows = self.data[self.dataBeginRow:]
        self.resultNames = self._parseResults()
        self.resultColors = helper.getCellColorsFromColumn(
            self.sheet, self.colorColumnIndex, self.dataBeginRow, len(self.data))

    def createResultStyles(self):
        """
        Create cell styles based on result names and their corresponding colors.
        """
        for index, resultName in enumerate(self.resultNames):
            color = self.resultColors[index]
            name = self._formatStyleName(resultName)
            styles.addCellStyle(name, color)

    def getResultStyleNames(self):
        results = []
        for resultName in self.resultNames:
            results.append([resultName, self._formatStyleName(resultName)])
        return results

    def _formatStyleName(self, resultName):
        return '({0})/{1}'.format('Result', resultName)

    def _parseResults(self):
        results = []
        for row in self.dataRows:
            if row[self.resultColumnIndex] != '':
                results.append(row[self.resultColumnIndex])
        return results
