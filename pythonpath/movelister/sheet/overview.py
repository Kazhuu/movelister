from movelister.core import cursor
from .sheet import Sheet
from movelister.format import filter
from movelister.model import Modifier, ModifiedAction


HEADER_ROW = 1
DATA_BEGIN_ROW = 2

NAME_COLUMN = 0
HIT_COLUMN = 1
FRAMES_COLUMN = 2
PHASE_COLUMN = 3
DEFAULT_COLUMN = 4

MODIFIER_START_COLUM_NAME = 'DEF'
MODIFIER_END_COLUM_NAME = 'Notes 1'


class Overview:

    def __init__(self, sheetName):
        # TODO: Init instance variables here to default values.
        self.name = sheetName
        self.modifiedActions = []

    @classmethod
    def fromSheet(cls, sheetName):
        instance = cls(sheetName)
        instance.readSheetContent()
        return instance

    def setActions(self, actions):
        self.actions = actions

    def readSheetContent(self):
        self.sheet = Sheet.getByName(self.name)
        self.data = cursor.getSheetContent(self.sheet)
        self.dataHeader = self.data[HEADER_ROW]
        self.dataRows = self.data[DATA_BEGIN_ROW:]
        self.modifierStartColumn = self.dataHeader.index(MODIFIER_START_COLUM_NAME) + 1
        self.modifierEndColumn = self.dataHeader.index(MODIFIER_END_COLUM_NAME)
        self.modifiers = self.dataHeader[self.modifierStartColumn:self.modifierEndColumn]
        self.actionNames = self._getUniqueActionNames()
        self.modifiedActions = self._readModifierAction()

    def getSheetContent(self):
        data = []
        for action in self.actions:
            data.append([action.name, action.phases])
        return data

    def _readModifiedActions(self):
        names = self._getUniqueActionNames()
        for name in names:
            rows = filter.filterRows(lambda row: row[NAME_COLUMN] == name, self.dataRows)
            self.modifiedActions.append(self._readModifierAction(rows))

    def _getUniqueActionNames(self):
        names = []
        for row in filter.filterRows(lambda row: row[NAME_COLUMN] != '', self.dataRows):
            if row[NAME_COLUMN] not in names:
                names.append(row[NAME_COLUMN])
        return names

    def _readModifierAction(self):
        groups = filter.groupRows(self.dataRows, NAME_COLUMN)
        for group in groups:
            self.modifiedActions.append(self._rowGroupToModifiedAction(group))

    def _rowGroupToModifiedAction(self, rowGroup):
        kwargs = {'name': rowGroup[0][NAME_COLUMN], 'phases': len(rowGroup)}
        modifiers = {}
        for phase, row in enumerate(rowGroup):
            if row[HIT_COLUMN] != '':
                kwargs['hitPhase'] = phase
            if row[DEFAULT_COLUMN] != '':
                kwargs['default'] = True
            modifiers[phase] = self._modifiersFromRow(row)
        return ModifiedAction(**kwargs)

    def _modifiersFromRow(self, row):
        mods = row[self.modifierStartColumn:self.modifierEndColumn]
        modifiers = []
        for index, value in enumerate(mods):
            if value != '':
                modifiers.append(Modifier(self.modifiers[index]))
        return modifiers
