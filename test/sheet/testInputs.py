from test import OfficeTestCase
from movelister.sheet import Inputs, INPUT_LIST_SHEET_NAME
from movelister.model import Input


class InputsTestCase(OfficeTestCase):

    def setUp(self):
        self.input = Inputs(INPUT_LIST_SHEET_NAME)
        self.inputList = self.input.getInputs()

    def testGetInputs(self):
        self.assertTrue(self.inputList)
        for mod in self.inputList:
            self.assertIsInstance(mod, Input)

    def testInputColor(self):
        firstActionColor = self.input.sheet.getCellByPosition(self.input.colorColumnIndex,
                                                              self.input.dataBeginRow).CellBackColor
        self.assertEqual(self.inputList[0].color, firstActionColor)
