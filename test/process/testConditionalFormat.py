from test.officeTestCase import OfficeTestCase
from movelister.sheet.sheet import Sheet
from movelister.core import names
from movelister.process import conditionalFormat
from movelister.sheet.master import Master
from movelister.sheet.inputs import Inputs
from movelister.sheet.results import Results
from movelister.sheet.sheet import MASTER_LIST_SHEET_NAME, RESULT_LIST_SHEET_NAME, INPUT_LIST_SHEET_NAME


class ConditionalFormatTestCase(OfficeTestCase):

    def setUp(self):
        super().setUp()
        self.view = 'Default'
        self.detailsName = names.getDetailsName(self.view)

    def testActionConditionalFormats(self):
        masterSheet = Master(MASTER_LIST_SHEET_NAME)
        detailsUnoSheet = Sheet.getByName(self.detailsName)
        actionConditionalFormat = conditionalFormat.createActionConditionalFormats(detailsUnoSheet, masterSheet, self.view)
        self.assertGreater(actionConditionalFormat.getCount(), 0)
        self.assertIn('Entry1', actionConditionalFormat.getElementNames())

    def testResultsConditionalFormats(self):
        resultsSheet = Results(RESULT_LIST_SHEET_NAME)
        detailsUnoSheet = Sheet.getByName(self.detailsName)
        resultsConditionalFormat = conditionalFormat.createResultsConditionalFormat(detailsUnoSheet, resultsSheet)
        self.assertGreater(resultsConditionalFormat.getCount(), 0)
        self.assertIn('Entry1', resultsConditionalFormat.getElementNames())

    def testInputsConditionalFormats(self):
        inputSheet = Inputs(INPUT_LIST_SHEET_NAME)
        detailsUnoSheet = Sheet.getByName(self.detailsName)
        inputsConditionalFormat = conditionalFormat.createInputsConditionalFormat(detailsUnoSheet, inputSheet, self.view)
        self.assertGreater(inputsConditionalFormat.getCount(), 0)
        self.assertIn('Entry1', inputsConditionalFormat.getElementNames())
