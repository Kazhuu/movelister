from test import OfficeTestCase
from movelister.sheet import Inputs, INPUT_LIST_SHEET_NAME
from movelister.model import Input
from movelister.sheet.inputs import COLOR_COLUMN, DATA_BEGIN_ROW


class InputsTestCase(OfficeTestCase):

    def setUp(self):
        self.input = Inputs(INPUT_LIST_SHEET_NAME)
        self.inputList = self.input.getInputs()

    def testGetInputs(self):
        self.assertTrue(self.inputList)
        for mod in self.inputList:
            self.assertIsInstance(mod, Input)

    def testInputColor(self):
        firstActionColor = self.input.sheet.getCellByPosition(COLOR_COLUMN, DATA_BEGIN_ROW).CellBackColor
        self.assertEqual(self.inputList[0].color, firstActionColor)
