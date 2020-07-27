from movelister.core import cursor, styles
from movelister.sheet.sheet import Sheet
from movelister.sheet import helper
from movelister.model.action import Action
from movelister.format import filter
from movelister.core import errors
from movelister.sheet.sheet import MASTER_LIST_SHEET_NAME

from collections import defaultdict
from collections import OrderedDict


class Master:

    def __init__(self, sheetName):
        self.name = sheetName
        self.sheet = Sheet.getByName(sheetName)
        self.data = cursor.getSheetContent(self.sheet)
        self.headerRowIndex = helper.getHeaderRowPosition(self.data)
        self.dataBeginRow = self.headerRowIndex + 1
        self.viewColumnIndex = helper.getColumnPosition(self.data, 'View', 0)
        self.inputsColumnIndex = helper.getColumnPosition(self.data, 'Input List', 1)
        self.nameColumnIndex = helper.getColumnPosition(self.data, 'Action Name', 2)
        self.colorColumnIndex = helper.getColumnPosition(self.data, 'Color', 3)
        self.phaseColumnIndex = helper.getColumnPosition(self.data, 'Phases', 4)
        self.dataHeader = self.data[self.headerRowIndex]
        self.dataRows = self.data[self.dataBeginRow:]
        self.actionColors = helper.getCellColorsFromColumn(
            self.sheet, self.colorColumnIndex, self.dataBeginRow, len(self.data))
        self.actions = self._parseActions()

    def getActions(self, view=None):
        if view:
            return [action for _, action in self.actions[view].items()]
        actionList = []
        for _, viewActions in self.actions.items():
            actionList.extend([action for _, action, in viewActions.items()])
        return actionList

    def findAction(self, view, name):
        """
        Find Action instance with given view name and action name from current Master sheet actions.
        If not found None is returned.
        """
        return self.actions[view].get(name, None)

    def getViewNames(self):
        """
        This function returns the names of the existing Views.
        """
        return self.actions.keys()

    def getOverviewName(self):
        """
        Return name from user input field on Master List sheet.
        """
        name = self.data[0][2]
        return name

    def createActionStyles(self):
        """
        Create cell styles to LibreOffice. One style per user defined action in
        the Master List sheet. Color column is used to define color for the style.
        """
        for viewName, actionsDict in self.actions.items():
            for action in actionsDict.values():
                name = self._formatStyleName(viewName, action.name)
                styles.addCellStyle(name, action.color)

    def getActionStyleNames(self, viewName):
        names = []
        for action in self.actions[viewName].values():
                names.append([action.name, self._formatStyleName(viewName, action.name)])
        return names

    def _formatStyleName(self, viewName, actionName):
            return '({0}/{1})/{2}'.format('Action', viewName, actionName)

    def _parseActions(self):
        actions = defaultdict(OrderedDict)
        for index, row in enumerate(self.dataRows):
            # Skip empty rows.
            if row[self.nameColumnIndex] != '':
                view = row[self.viewColumnIndex]
                kwargs = self._rowToKwargs(row)
                kwargs['color'] = self.actionColors[index]
                self._actionExist(actions, view, kwargs['name'])
                actions[view][kwargs['name']] = Action(**kwargs)
        return actions

    def _actionExist(self, actions, view, actionName):
        """
        Check that no duplicate case-insensitive action name already exist for
        given name. If does then raise DuplicateError.
        """
        if actionName.lower() in map(str.lower, actions[view].keys()):
            msg = ('Case-insensitive duplicate action named "{0}" in view "{1}" '
                   'already exists in the {2} sheet. To fix make sure no case-insensitive '
                   'actions with the same exist in the same view.'
            ).format(actionName, view, MASTER_LIST_SHEET_NAME)
            raise errors.DuplicateError(MASTER_LIST_SHEET_NAME, msg)

    def _rowToKwargs(self, row):
        kwargs = {'name': row[self.nameColumnIndex]}
        if row[self.inputsColumnIndex] != '':
            kwargs['inputs'] = row[self.inputsColumnIndex]
        if row[self.phaseColumnIndex] != '':
            kwargs['phases'] = int(row[self.phaseColumnIndex])
        return kwargs
