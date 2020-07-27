from movelister.sheet.sheet import Sheet
from movelister.sheet import helper
from movelister.core import cursor, styles
from movelister.model.input import Input
from movelister.format import filter

from collections import defaultdict


class Inputs:

    def __init__(self, sheetName):
        self.name = sheetName
        self.sheet = Sheet.getByName(sheetName)
        self.data = cursor.getSheetContent(self.sheet)
        self.headerRowIndex = helper.getHeaderRowPosition(self.data)
        self.dataBeginRow = self.headerRowIndex + 1
        self.inputsColumnIndex = helper.getColumnPosition(self.data, 'Input List', 0)
        self.nameColumnIndex = helper.getColumnPosition(self.data, 'Input Name', 1)
        self.buttonColumnIndex = helper.getColumnPosition(self.data, 'Button', 2)
        self.colorColumnIndex = helper.getColumnPosition(self.data, 'Color', 3)
        self.dataHeader = self.data[self.headerRowIndex]
        self.dataRows = self.data[self.dataBeginRow:]
        self.inputColors = helper.getCellColorsFromColumn(
            self.sheet, self.colorColumnIndex, self.dataBeginRow, len(self.data)
        )
        self.inputs = self._parseInputs()

    def getInputNames(self, viewName='Default'):
        return [instance.name for instance in self.inputs[viewName]]

    def getInputs(self, viewName=None):
        """
        Return list of Input class instances using given view. If view is not
        given then return all inputs as a list.
        """
        if viewName:
            return self.inputs[viewName]
        inputs = []
        for inputList in self.inputs.values():
            inputs.extend(inputList)
        return inputs

    def createInputStyles(self):
        """
        Create cell styles based on used defined input names and their colors.
        """
        for viewName, inputs in self.inputs.items():
            for inputInstance in inputs:
                name = self._formatStyleName(viewName, inputInstance.name)
                styles.addCellStyle(name, inputInstance.color)

    def getInputStylesNames(self):
        stylesPairs = []
        for viewName, inputs in self.inputs.items():
            for inputInstance in inputs:
                stylesPairs.append([inputInstance.name, self._formatStyleName(viewName, inputInstance.name)])
        return stylesPairs

    def _formatStyleName(self, viewName, inputName):
        return '({0}/{1})/{2}'.format('Input', viewName, inputName)

    def _parseInputs(self):
        inputs = defaultdict(list)
        for index, row in enumerate(self.dataRows):
            if row[self.nameColumnIndex] != '':
                kwargs = self._rowToKwargs(row)
                kwargs['color'] = self.inputColors[index]
                viewName = row[self.inputsColumnIndex]
                inputs[viewName].append(Input(**kwargs))
        return inputs

    def _rowToKwargs(self, row):
        kwargs = {'name': row[self.nameColumnIndex]}
        return kwargs
