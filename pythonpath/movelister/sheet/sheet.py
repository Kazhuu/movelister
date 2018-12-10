from movelister.core import Context


OVERVIEW_SHEET_NAME = 'Overview (Old)'
MASTER_LIST_SHEET_NAME = 'Master List'
INPUT_LIST_SHEET_NAME = 'Inputs'
DETAILS_SHEET_NAME = 'Details (Old)'
MODIFIER_LIST_SHEET_NAME = 'Modifiers'
MODIFIER_LIST_OLD_SHEET_NAME = 'Modifier List (Old)'
RESULT_LIST_SHEET_NAME = 'Results List'
ABOUT_SHEET_NAME = 'About'


class Sheet():
    """
    Class to abstract all operations related to different sheets in the
    document.
    """

    @classmethod
    def getOverviewSheet(cls):
        return Context.getDocument().Sheets.getByName(OVERVIEW_SHEET_NAME)

    @classmethod
    def getMasterSheet(cls):
        return Context.getDocument().Sheets.getByName(MASTER_LIST_SHEET_NAME)

    @classmethod
    def getInputSheet(cls):
        return Context.getDocument().Sheets.getByName(INPUT_LIST_SHEET_NAME)

    @classmethod
    def getDetailsSheet(cls):
        return Context.getDocument().Sheets.getByName(DETAILS_SHEET_NAME)

    @classmethod
    def getModifierSheet(cls):
        return Context.getDocument().Sheets.getByName(MODIFIER_LIST_SHEET_NAME)

    @classmethod
    def getModifierSheetOld(cls):
        return Context.getDocument().Sheets.getByName(MODIFIER_LIST_OLD_SHEET_NAME)

    @classmethod
    def getResultSheet(cls):
        return Context.getDocument().Sheets.getByName(RESULT_LIST_SHEET_NAME)

    @classmethod
    def getAboutSheet(cls):
        return Context.getDocument().Sheets.getByName(ABOUT_SHEET_NAME)

    @classmethod
    def getByName(cls, name):
        """
        Get sheet by given name.
        """
        return Context.getDocument().Sheets.getByName(name)

    @classmethod
    def newSheet(cls, name, position):
        """
        Creates new sheet with given name to given position and returns it.
        """
        Context.getDocument().Sheets.insertNewByName(name, position)
        return cls.getByName(name)

    @classmethod
    def newSheetRightOf(cls, rightOfName, newName):
        position = cls.getPosition(rightOfName)
        return cls.newSheet(newName, position + 1)

    @classmethod
    def newSheetLeftOf(cls, leftOfName, newName):
        position = cls.getPosition(leftOfName)
        return cls.newSheet(newName, position)

    @classmethod
    def getPosition(cls, name):
        sheets = cls.getSheetNames()
        return sheets.index(name)

    @classmethod
    def getSheetNames(cls):
        """
        Return list of sheet names in current file.
        """
        return Context.getDocument().Sheets.getElementNames()
