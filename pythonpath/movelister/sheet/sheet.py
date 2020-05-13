from com.sun.star.container import NoSuchElementException

from movelister.core.context import Context


OVERVIEW_TEMPLATE_NAME = 'Overview Template'
DETAILS_TEMPLATE_NAME = 'Details Template'

OVERVIEW_SHEET_NAME = 'Overview'
MASTER_LIST_SHEET_NAME = 'Master List'
INPUT_LIST_SHEET_NAME = 'Inputs'
DETAILS_SHEET_NAME = 'Details'
MODIFIER_LIST_SHEET_NAME = 'Modifiers'
RESULT_LIST_SHEET_NAME = 'Results'
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
    def getResultSheet(cls):
        return Context.getDocument().Sheets.getByName(RESULT_LIST_SHEET_NAME)

    @classmethod
    def getAboutSheet(cls):
        return Context.getDocument().Sheets.getByName(ABOUT_SHEET_NAME)

    @classmethod
    def deleteSheetByName(cls, name):
        """
        Delete sheet from the document by given name. Return true on success,
        false otherwise.
        """
        try:
            Context.getDocument().Sheets.removeByName(name)
            return True
        except NoSuchElementException:
            return False

    @classmethod
    def getByName(cls, name):
        """
        Get sheet by given name, if not found raise NoSuchElementException.
        """
        return Context.getDocument().Sheets.getByName(name)

    @classmethod
    def hasByName(cls, name):
        """
        Return true if document has sheet with given name, false otherwise.
        """
        try:
            cls.getByName(name)
            return True
        except NoSuchElementException:
            return False

    @classmethod
    def getByPosition(cls, position):
        """
        Return sheet by given position.
        """
        return Context.getDocument().Sheets.getByIndex(position)

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
    def newOverview(cls, name):
        """
        Insert new Overview sheet right of Master sheet with given name put
        inside of parentheses. Returns created sheet.

        Sheet with given name must not exist, otherwise RuntimeException is
        raised.
        """
        position = cls.getPosition(MASTER_LIST_SHEET_NAME) + 1
        sheetName = '{0} ({1})'.format(OVERVIEW_SHEET_NAME, name)
        Context.getDocument().Sheets.copyByName(OVERVIEW_TEMPLATE_NAME, sheetName, position)
        return cls.getByPosition(position)

    @classmethod
    def newDetails(cls, overviewName, detailsName):
        """
        Insert new Details sheet right of the given overview sheet. New details
        sheet will have given detailsName in parentheses.

        Sheet with given name must not exist, otherwise RuntimeException is
        raised.
        """
        position = cls.getPosition(overviewName) + 1
        sheetName = '{0} ({1})'.format(DETAILS_SHEET_NAME, detailsName)
        Context.getDocument().Sheets.copyByName(DETAILS_TEMPLATE_NAME, sheetName, position)
        return cls.getByPosition(position)

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
