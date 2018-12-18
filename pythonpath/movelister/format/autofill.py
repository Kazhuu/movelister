from movelister.core import cursor
from movelister.sheet import helper, master, inputs


def autoFillMasterList(masterList):
    '''
    This function looks at the rows in Master List and fills certain empty fields.
    It's mainly for user convenience if they work with 'Default' values.
    '''
    for row in masterList.data[master.DATA_BEGIN_ROW:]:
        if row[master.NAME_COLUMN] != '':
            if row[master.VIEW_COLUMN] == '':
                row[master.VIEW_COLUMN] = 'Default'
            if row[master.INPUTS_COLUMN] == '':
                row[master.INPUTS_COLUMN] = 'Default'
            if row[master.PHASE_COLUMN] == '':
                row[master.PHASE_COLUMN] = '0'
    cursor.setSheetContent(masterList.sheet, masterList.data)


def autoFillOverview():
    '''
    A function that checks if the Phases column is correctly filled in an Overview before generating.
    '''
    print()


def autoFillInputs(inputList):
    '''
    A function that checks if Input List column is properly filled in Inputs before generating.
    If a row has a Name but no Input List, then the latter field is filled with 'Default'.
    '''
    for row in inputList.data[inputs.DATA_BEGIN_ROW:]:
        if row[inputs.NAME_COLUMN] != '':
            if row[inputs.INPUT_LIST_NAME_COLUMN] == '':
                row[inputs.INPUT_LIST_NAME_COLUMN] = 'Default'
    cursor.setSheetContent(inputList.sheet, inputList.data)


def generateDefaultInputs(inputList):
    '''
    A function that creates an Input List called 'Default' if the Inputs is currently empty.
    '''
    if len(inputList.dataRows) == 0:
        length = len(inputList.data[0])
        input1 = helper.createEmptyRow(length)
        input2 = helper.createEmptyRow(length)
        input3 = helper.createEmptyRow(length)
        input4 = helper.createEmptyRow(length)
        input5 = helper.createEmptyRow(length)
        input6 = helper.createEmptyRow(length)

        input1[inputs.NAME_COLUMN] = 'Letting go of input'
        input2[inputs.NAME_COLUMN] = 'Move'
        input2[inputs.INPUT_COLUMN] = 'WASD / L-stick'
        input3[inputs.NAME_COLUMN] = 'Jump'
        input3[inputs.INPUT_COLUMN] = 'Space / X'
        input4[inputs.NAME_COLUMN] = 'Roll'
        input5[inputs.NAME_COLUMN] = 'Attack'
        input6[inputs.NAME_COLUMN] = 'Block'

        inputList.data.append(input1)
        inputList.data.append(input2)
        inputList.data.append(input3)
        inputList.data.append(input4)
        inputList.data.append(input5)
        inputList.data.append(input6)

        cursor.setSheetContent(inputList.sheet, inputList.data)
