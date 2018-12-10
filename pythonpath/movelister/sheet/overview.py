from movelister.core import cursor
from .sheet import Sheet
from movelister.format import filter


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
        self.modifiers = self._readModifierNames()
        self.actionNames = self._getUniqueActionNames()

    def getSheetContent(self):
        data = []
        for action in self.actions:
            data.append([action.name, action.phases])
        return data

    def _readModifierNames(self):
        start = self.dataHeader.index(MODIFIER_START_COLUM_NAME)
        end = self.dataHeader.index(MODIFIER_END_COLUM_NAME)
        return self.dataHeader[start + 1:end]

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

    def _readModifierAction(self, actionRows):
        # TODO: Write this next
        pass
