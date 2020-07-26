from test.officeTestCase import OfficeTestCase
from movelister.sheet.inputs import Inputs
from movelister.sheet.sheet import INPUT_LIST_SHEET_NAME
from movelister.model.input import Input
from movelister.core import styles


class InputsTestCase(OfficeTestCase):

    def setUp(self):
        super().setUp()
        self.inputSheet = Inputs(INPUT_LIST_SHEET_NAME)

    def testGetInputNames(self):
        inputNames = self.inputSheet.getInputNames()
        self.assertIn('Move', inputNames)

    def testGetInputs(self):
        inputList = self.inputSheet.getInputs()
        self.assertTrue(inputList)
        for mod in inputList:
            self.assertIsInstance(mod, Input)

    def testCreateInputStyles(self):
        styles.removeNonDefaultStyles()
        cellStyles = styles.getNonDefaultStyles()
        self.assertFalse(cellStyles)

        self.inputSheet.createInputStyles()
        cellStyles = styles.getNonDefaultStyles()
        self.assertIn('(Input/Default)/Move', cellStyles)
