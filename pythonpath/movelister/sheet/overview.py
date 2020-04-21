from movelister.core import cursor
from movelister.core.iterator import DetailsIterator
from movelister.sheet.sheet import Sheet
from movelister.format import filter
from movelister.model.modifier import Modifier
from movelister.model.action import Action
from movelister.sheet import helper


MODIFIER_START_COLUMN_NAME = 'DEF'
MODIFIER_END_COLUMN_NAME = 'Notes 1'


class Overview:
    """
    Class representing Overview sheet in the movelister document. Class
    abstracts content presented from two dimensional array to more easily
    understandable form.
    """

    def __init__(self, sheetName):
        """
        Instantiate empty Overview sheet with given name.
        """
        self.name = sheetName
        self._modifiers = []
        self._actions = []

    @classmethod
    def fromSheet(cls, sheetName):
        """
        Instantiate this class by reading given Overview sheet content and
        extracting data from it.
        """
        instance = cls(sheetName)
        instance._readSheetContent()
        return instance

    @property
    def modifiers(self):
        return self._modifiers

    @modifiers.setter
    def modifiers(self, value):
        self._modifiers = value

    @property
    def actions(self):
        return self._actions

    @actions.setter
    def actions(self, value):
        self._actions = value

    def addModifier(self, modifier):
        self._modifiers.append(modifier)

    def addAction(self, action):
        self._actions.append(action)

    def findAction(self, comparedAction):
        """
        Find given action from the set of actions. If none is found, None is
        returned. Actions are considered equal if their names are equal.
        """
        return next((action for action in self._actions if action == comparedAction), None)

    def iterateActions(self):
        """
        Return iterator to iterate over actions.
        """
        return ActionsIterator(self.actions)

    def _readSheetContent(self):
        self.sheet = Sheet.getByName(self.name)
        self.data = cursor.getSheetContent(self.sheet)
        self.headerRowIndex = helper.getHeaderRowPosition(self.data)
        self.dataBeginRow = self.headerRowIndex + 1
        self.nameColumnIndex = helper.getColumnPosition(self.data, 'Action Name')
        self.hitColumnIndex = helper.getColumnPosition(self.data, 'Hit')
        self.framesColumnIndex = helper.getColumnPosition(self.data, 'Frames')
        self.phaseColumnIndex = helper.getColumnPosition(self.data, 'Phase')
        self.defaultColumnIndex = helper.getColumnPosition(self.data, 'DEF')
        self.notesIndex1 = helper.getColumnPosition(self.data, 'Notes 1')
        self.notesIndex2 = helper.getColumnPosition(self.data, 'Notes 2')
        self.notesIndex3 = helper.getColumnPosition(self.data, 'Notes 3')
        self.dataHeader = self.data[self.headerRowIndex]
        self.dataRows = self._dataRows()
        self.modifierStartColumn = self.dataHeader.index(MODIFIER_START_COLUMN_NAME) + 1
        self.modifierEndColumn = self.dataHeader.index(MODIFIER_END_COLUMN_NAME)
        self.modifiers = self._readModifiers()
        self.actionNames = self._getUniqueActionNames()
        self._actions = self._readActions()

    def _dataRows(self):
        data = self.data[self.dataBeginRow:]
        return helper.stripTrailingEmptyRows(data)

    def _readModifiers(self):
        modifiers = []
        mods = self.dataHeader[self.modifierStartColumn:self.modifierEndColumn]
        for mod in mods:
            modifiers.append(Modifier(mod))
        return modifiers

    def _getUniqueActionNames(self):
        names = []
        for row in filter.filterRows(lambda row: row[self.nameColumnIndex] != '', self.dataRows):
            if row[self.nameColumnIndex] not in names:
                names.append(row[self.nameColumnIndex])
        return names

    def _readActions(self):
        actions = []
        groups = filter.groupRows(self.dataRows, self.nameColumnIndex)
        for group in groups:
            actions.append(self._rowGroupToAction(group))
        return actions

    def _rowGroupToAction(self, rowGroup):
        modifiers = {}
        notes = {}
        kwargs = {'name': rowGroup[0][self.nameColumnIndex], 'phases': len(rowGroup),
                  'modifiers': modifiers, 'notes': notes}
        for phase, row in enumerate(rowGroup):
            if row[self.hitColumnIndex] != '':
                kwargs['hitPhase'] = phase
            if row[self.defaultColumnIndex] != '':
                kwargs['default'] = True
            modInstances = self._modifiersFromRow(row)
            if modInstances:
                modifiers[phase] = modInstances
            noteInstances = self._notesFromRow(row)
            if noteInstances:
                notes[phase] = noteInstances
        return Action(**kwargs)

    def _modifiersFromRow(self, row):
        mods = row[self.modifierStartColumn:self.modifierEndColumn]
        modifierNames = self.dataHeader[self.modifierStartColumn:self.modifierEndColumn]
        modifiers = []
        for index, value in enumerate(mods):
            if value != '':
                modifiers.append(Modifier(modifierNames[index]))
        return modifiers

    def _notesFromRow(self, row):
        notes = row[self.notesIndex1:self.notesIndex3 + 1]
        noteList = []
        for index, value in enumerate(notes):
            noteList.append(value)
        return noteList
