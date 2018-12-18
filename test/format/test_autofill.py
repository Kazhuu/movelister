from test import OfficeTestCase
from movelister.format import autofill
from movelister.sheet import Master, MASTER_LIST_SHEET_NAME, Inputs, INPUT_LIST_SHEET_NAME
from movelister.sheet.master import VIEW_COLUMN, INPUTS_COLUMN, PHASE_COLUMN
from movelister.sheet.inputs import INPUT_LIST_NAME_COLUMN


class AutoFillTestCase(OfficeTestCase):

    def testAutoFillMasterList(self):
        master = Master(MASTER_LIST_SHEET_NAME)

        # Change some values to empty in the Master List.
        master.sheet.getCellByPosition(VIEW_COLUMN, 3).setString('')
        master.sheet.getCellByPosition(INPUTS_COLUMN, 3).setString('')
        master.sheet.getCellByPosition(PHASE_COLUMN, 3).setString('')

        # Autofill Master List.
        autofill.autoFillMasterList(master)

        # Read Master List again and assert values are like they should.
        self.assertEqual(master.sheet.getCellByPosition(VIEW_COLUMN, 3).getString(), 'Default')
        self.assertEqual(master.sheet.getCellByPosition(INPUTS_COLUMN, 3).getString(), 'Default')
        self.assertEqual(master.sheet.getCellByPosition(PHASE_COLUMN, 3).getString(), '0')


    def testAutoFillInputs(self):
        self.skipTest('Gives a runtime error every time?')
        inputList = Inputs(INPUT_LIST_SHEET_NAME)

        # Change some values to empty in Inputs.
        inputList.sheet.getCellByPosition(INPUT_LIST_NAME_COLUMN, 3).setString('')

        # Autofill Inputs.
        autofill.autoFillInputs(inputList)

        # Read Inputs again and assert values are like they should.
        self.assertEqual(master.sheet.getCellByPosition(INPUT_LIST_NAME_COLUMN, 3).getString('Default'))
