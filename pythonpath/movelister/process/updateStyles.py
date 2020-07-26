from movelister.sheet.results import Results
from movelister.sheet.inputs import Inputs
from movelister.sheet.master import Master
from movelister.sheet.sheet import MASTER_LIST_SHEET_NAME
from movelister.sheet.sheet import RESULT_LIST_SHEET_NAME
from movelister.sheet.sheet import INPUT_LIST_SHEET_NAME
from movelister.core import styles


class UpdateStyles:
    """
    Class responsible to update all Movelister used cell styles in the
    LibreOffice document.
    """

    @classmethod
    def update(cls):
        """
        Remove all old non-default styles and create new ones from sheets
        Results, Inputs and Master List.
        """
        cls.resultsSheet = Results(RESULT_LIST_SHEET_NAME)
        cls.inputsSheet = Inputs(INPUT_LIST_SHEET_NAME)
        cls.masterSheet = Master(MASTER_LIST_SHEET_NAME)
        cls._removeOldStyles()
        cls._createStyles()

    @classmethod
    def _removeOldStyles(cls):
        styles.removeNonDefaultStyles()

    @classmethod
    def _createStyles(cls):
        cls.inputsSheet.createInputStyles()
        cls.resultsSheet.createResultStyles()
        cls.masterSheet.createActionStyles()
