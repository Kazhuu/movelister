from movelister.context import Context


MASTER_ACTION_LIST_SHEET_NAME = 'Master Action List'
INPUT_LIST_SHEET_NAME = 'Input Lists'
MECHANICS_LIST_SHEET_NAME = 'Mechanics Test'
SIMULTANEOUS_TEST_SHEET_NAME = 'Simultaneous Test'
MODIFIER_LIST_SHEET_NAME = 'Modifier List'
RESULT_LIST_SHEET_NAME = 'Results List'
TARGET_LIST_SHEET_NAME = 'Target List'
ABOUT_SHEET_NAME = 'About'


class Sheet():
    """
    Class to abstract all operations related to different sheets in the
    document.
    """

    @classmethod
    def getMasterActionList(cls):
        return Context.getDocument().Sheets.getByName(MASTER_ACTION_LIST_SHEET_NAME)

    @classmethod
    def getInputList(cls):
        return Context.getDocument().Sheets.getByName(INPUT_LIST_SHEET_NAME)

    @classmethod
    def getMechanicsList(cls):
        return Context.getDocument().Sheets.getByName(MECHANICS_LIST_SHEET_NAME)

    @classmethod
    def getSimultaneousTest(cls):
        return Context.getDocument().Sheets.getByName(SIMULTANEOUS_TEST_SHEET_NAME)

    @classmethod
    def getModifierList(cls):
        return Context.getDocument().Sheets.getByName(MODIFIER_LIST_SHEET_NAME)

    @classmethod
    def getResultsList(cls):
        return Context.getDocument().Sheets.getByName(RESULT_LIST_SHEET_NAME)

    @classmethod
    def getTargetList(cls):
        return Context.getDocument().Sheets.getByName(TARGET_LIST_SHEET_NAME)

    @classmethod
    def getAbout(cls):
        return Context.getDocument().Sheets.getByName(ABOUT_SHEET_NAME)
