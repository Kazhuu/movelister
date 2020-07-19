from com.sun.star.container import NoSuchElementException

from movelister.core.context import Context
from movelister.ui import message_box

OVERVIEW_TEMPLATE_NAME = 'Overview Template'
DETAILS_TEMPLATE_NAME = 'Details Template'

MASTER_LIST_SHEET_NAME = 'Master List'
INPUT_LIST_SHEET_NAME = 'Inputs'
MODIFIER_LIST_SHEET_NAME = 'Modifiers'
RESULT_LIST_SHEET_NAME = 'Results'
ABOUT_SHEET_NAME = 'About'


class Sheet():
    """
    Class to abstract all operations related to different sheets in the
    document.
    """

    @classmethod
    def getMasterSheet(cls):
        return Context.getDocument().Sheets.getByName(MASTER_LIST_SHEET_NAME)

    @classmethod
    def getInputSheet(cls):
        return Context.getDocument().Sheets.getByName(INPUT_LIST_SHEET_NAME)

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
    def newOverview(cls, name, position):
        """
        Insert new Overview sheet with given name to the given position.
        Returns created sheet UNO object.

        Sheet with given name must not exist, otherwise RuntimeException is
        raised.
        """
        Context.getDocument().Sheets.copyByName(OVERVIEW_TEMPLATE_NAME, name, position)
        return cls.getByPosition(position)

    @classmethod
    def newDetails(cls, overviewName, name):
        """
        Insert new Details sheet with given name right of the given overview sheet.

        Sheet with given name must not exist, otherwise RuntimeException is
        raised.
        """
        position = cls.getPosition(overviewName) + 1
        Context.getDocument().Sheets.copyByName(DETAILS_TEMPLATE_NAME, name, position)
        return cls.getByPosition(position)

    @classmethod
    def getPosition(cls, name):
        """
        Document can contain many sheets. Return index of the sheet with given
        name. If not found None is returned instead.
        """
        sheets = cls.getSheetNames()
        try:
            return sheets.index(name)
        except ValueError:
            return None

    @classmethod
    def getSheetNames(cls):
        """
        Return list of sheet names in current document.
        """
        return Context.getDocument().Sheets.getElementNames()

    @classmethod
    def checkTemplatesExists(cls):
        """
        Return true if all needed template sheets exists for this document, false otherwise.
        """
        return Sheet.hasByName('Overview Template') and Sheet.hasByName('Details Template')
