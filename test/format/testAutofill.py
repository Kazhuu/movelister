import pdb
from test.officeTestCase import OfficeTestCase
from movelister.format import autofill
from movelister.sheet.sheet import MASTER_LIST_SHEET_NAME, INPUT_LIST_SHEET_NAME
from movelister.sheet.master import Master
from movelister.sheet.inputs import Inputs


class AutoFillTestCase(OfficeTestCase):

    def testAutoFillMasterList(self):
        self.skipTest('Outdated code, doesn\'t need to be tested.')
        master = Master(MASTER_LIST_SHEET_NAME)

        # Change some values to empty in the Master List.
        cell1 = master.sheet.getCellByPosition(master.viewColumnIndex, 3)
        cell2 = master.sheet.getCellByPosition(master.inputsColumnIndex, 3)
        cell3 = master.sheet.getCellByPosition(master.phaseColumnIndex, 3)

        cell1.setString('')
        cell2.setString('')
        cell3.setString('')

        # Autofill Master List.
        autofill.autoFillMasterList(master)

        # Read Master List again and assert values are like they should.
        self.assertEqual(cell1.getString(), 'Default')
        self.assertEqual(cell2.getString(), 'Default')
        self.assertEqual(cell3.getString(), '0')

    def testAutoFillInputs(self):
        self.skipTest('Outdated code, doesn\'t need to be tested.')
        inputList = Inputs(INPUT_LIST_SHEET_NAME)

        # Change some values to empty in Inputs.
        inputList.sheet.getCellByPosition(INPUT_LIST_NAME_COLUMN, 3).setString('')

        # Autofill Inputs.
        autofill.autoFillInputs(inputList)

        # Read Inputs again and assert values are like they should.
        self.assertEqual(master.sheet.getCellByPosition(INPUT_LIST_NAME_COLUMN, 3).getString('Default'))
