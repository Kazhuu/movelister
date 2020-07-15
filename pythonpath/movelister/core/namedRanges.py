from movelister.core import cursor
from movelister.core.context import Context
from movelister.format import convert
from movelister.sheet.sheet import Sheet
from com.sun.star.uno import RuntimeException

import re

class NamedRanges:

    def __init__(self, UnoSheet, column, viewName):
        self.sheet = UnoSheet
        self.sheetName = self.sheet.Name
        self.column = column
        self.viewName = viewName
        self.namedRanges = Context.getDocument().NamedRanges
        self.sheetData = cursor.getColumn(self.sheet, self.column)
        self.cellAddress = self.sheet.getCellByPosition(1, 1).getCellAddress()

    def generate(self):
        self._deleteNamedRanges()
        self._createNamedRanges()

    def _deleteNamedRanges(self):
        """
        Delete old named ranged related to this view.
        """
        namedRangesList = self.namedRanges.getElementNames()
        pattern = re.compile(r'\(' + re.escape(self.viewName) + r'\)$')
        for name in namedRangesList:
            if pattern.search(name):
                self.namedRanges.removeByName(name)

    def _createNamedRanges(self):
        """
        This function goes through a column in a sheet and assigns named ranges
        on regions when column content changes.
        """
        currentAction = self.sheetData[1]
        regionStartRow = 2
        for index, line in enumerate(self.sheetData[1:]):
            if line and line != currentAction:
                namedRangeName = self._getName(currentAction, self.viewName)
                regionEndRow = index
                self._createNamedRange(namedRangeName, regionStartRow, regionEndRow)
                regionStartRow = index + 2
                currentAction = line
        namedRangeName = self._getName(currentAction, self.viewName)
        self._createNamedRange(namedRangeName, regionStartRow, len(self.sheetData))

    def _createNamedRange(self, name, startRow, endRow):
        """
        A function that creates a new named range.
        """
        address = self.sheet.getCellByPosition(1, 1)
        formula = self._buildFormulaExpression(startRow, endRow)
        try:
            self.namedRanges.addNewByName(name, formula, self.cellAddress, 0)
        except RuntimeException:
            print('Movelister: case insensitive named range with name "{0}" already exist'.format(name))

    def _buildFormulaExpression(self, startRow, endRow):
        """
        Build formula expression used to for the named range. Notice that
        counting for index starts from 1, not from 0.
        """
        columnBaseAddress = convert.convertIntoBaseAddress(self.column + 1)
        return '$\'' + self.sheetName + '\'.' + '$' + columnBaseAddress + '$' + str(startRow) + ':' + '$' + columnBaseAddress + '$' + str(endRow)

    def _getName(self, actionName, viewName):
        """
        Build name used for the named range.
        """
        return '{0} ({1})'.format(actionName, viewName)
