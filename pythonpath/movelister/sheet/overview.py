from movelister.core import cursor
from .sheet import Sheet
from movelister.format import filter
from movelister.model import Modifier, ModifiedAction
from movelister.sheet import helper


MODIFIER_START_COLUMN_NAME = 'DEF'
MODIFIER_END_COLUMN_NAME = 'Notes 1'


class Overview:

    def __init__(self, sheetName):
        self.name = sheetName
        self.modifiers = []
        self.modifiedActions = []

    @classmethod
    def fromSheet(cls, sheetName):
        instance = cls(sheetName)
        instance.readSheetContent()
        return instance

    def readSheetContent(self):
        self.sheet = Sheet.getByName(self.name)
        self.data = cursor.getSheetContent(self.sheet)
        self.headerRowIndex = helper.getHeaderRowPosition(self.data)
        self.dataBeginRow = self.headerRowIndex + 1
        self.nameColumnIndex = helper.getColumnPosition(self.data, 'Action Name')
        self.hitColumnIndex = helper.getColumnPosition(self.data, 'Hit')
        self.framesColumnIndex = helper.getColumnPosition(self.data, 'Frames')
        self.phaseColumnIndex = helper.getColumnPosition(self.data, 'Phase')
        self.defaultColumnIndex = helper.getColumnPosition(self.data, 'DEF')
        self.dataHeader = self.data[self.headerRowIndex]
        self.dataRows = self.data[self.dataBeginRow:]
        self.modifierStartColumn = self.dataHeader.index(MODIFIER_START_COLUMN_NAME) + 1
        self.modifierEndColumn = self.dataHeader.index(MODIFIER_END_COLUMN_NAME)
        self.modifiers = self._readModifiers()
        self.actionNames = self._getUniqueActionNames()
        self.modifiedActions = self._readModifiedActions()

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

    def _readModifiedActions(self):
        modifiedActions = []
        groups = filter.groupRows(self.dataRows, self.nameColumnIndex)
        for group in groups:
            modifiedActions.append(self._rowGroupToModifiedAction(group))
        return modifiedActions

    def _rowGroupToModifiedAction(self, rowGroup):
        modifiers = {}
        kwargs = {'name': rowGroup[0][self.nameColumnIndex], 'phases': len(rowGroup), 'modifiers': modifiers}
        for phase, row in enumerate(rowGroup):
            if row[self.hitColumnIndex] != '':
                kwargs['hitPhase'] = phase
            if row[self.defaultColumnIndex] != '':
                kwargs['default'] = True
            modInstances = self._modifiersFromRow(row)
            if modInstances:
                modifiers[phase] = modInstances
        return ModifiedAction(**kwargs)

    def _modifiersFromRow(self, row):
        mods = row[self.modifierStartColumn:self.modifierEndColumn]
        modifierNames = self.dataHeader[self.modifierStartColumn:self.modifierEndColumn]
        modifiers = []
        for index, value in enumerate(mods):
            if value != '':
                modifiers.append(Modifier(modifierNames[index]))
        return modifiers
