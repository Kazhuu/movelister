from movelister.core import cursor
from .sheet import Sheet


class Overview:

    def __init__(self, sheetName):
        self.name = sheetName

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

    def getSheetContent(self):
        data = []
        for action in self.actions:
            data.append([action.name, action.phases])
        return data
