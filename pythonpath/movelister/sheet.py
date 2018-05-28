from movelister import environment


MASTER_ACTION_LIST_SHEET_NAME = 'Master Action List'
INPUT_LIST_SHEET_NAME = 'Input Lists'
MECHANICS_LIST_SHEET_NAME = 'Mechanics Test'
SIMULTANEOUS_TEST_SHEET_NAME = 'Simultaneous Test'
MODIFIER_LIST_SHEET_NAME = 'Modifier List'
RESULT_LIST_SHEET_NAME = 'Results List'
TARGET_LIST_SHEET_NAME = 'Target List'
ABOUT_SHEET_NAME = 'About'


class Sheet:
    """
    Class to abstract all operations related to different sheets in the
    document.
    """

    def __init__(self, **kwargs):
        self.sheets = environment.getDocument(**kwargs).Sheets

    def getMasterActionList(self):
        return self.sheets.getByName(MASTER_ACTION_LIST_SHEET_NAME)

    def getInputList(self):
        return self.sheets.getByName(INPUT_LIST_SHEET_NAME)

    def getMasterActionList(self):
        return self.sheets.getByName(MECHANICS_LIST_SHEET_NAME)

    def getSimultaneousTest(self):
        return self.sheets.getByName(SIMULTANEOUS_TEST_SHEET_NAME)

    def getModifierList(self):
        return self.sheets.getByName(MODIFIER_LIST_SHEET_NAME)

    def getResultsList(self):
        return self.sheets.getByName(RESULT_LIST_SHEET_NAME)

    def getTargetList(self):
        return self.sheets.getByName(TARGET_LIST_SHEET_NAME)

    def getAbout(self):
        return self.sheets.getByName(ABOUT_SHEET_NAME)
