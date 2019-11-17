from movelister.core import cursor
from movelister.sheet import helper


def autoFillMasterList(masterList):
    """
    NOTE: this entire module is old code that is incompatible with the current vision of Movelister.
    But the basic idea is good, should be incorporated into the list generating.

    This function looks at the rows in Master List and fills certain empty fields.
    It's mainly for user convenience if they work with 'Default' values.
    """
    for row in masterList.data[masterList.dataBeginRow:]:
        if row[masterList.nameColumnIndex] != '':
            if row[masterList.viewColumnIndex] == '':
                row[masterList.viewColumnIndex] = 'Default'
            if row[masterList.inputsColumnIndex] == '':
                row[masterList.inputsColumnIndex] = 'Default'
            if row[masterList.phaseColumnIndex] == '':
                row[masterList.phaseColumnIndex] = '0'
    cursor.setSheetContent(masterList.sheet, masterList.data)


def autoFillOverview():
    """
    A function that checks if the Phases column is correctly filled in an Overview before generating.
    """
    print()


def autoFillInputs(inputList):
    """
    A function that checks if Input List column is properly filled in Inputs before generating.
    If a row has a Name but no Input List, then the latter field is filled with 'Default'.
    """
    for row in inputList.data[inputList.dataBeginRow:]:
        if row[inputList.nameColumnIndex] != '':
            if row[inputList.inputsColumnIndex] == '':
                row[inputList.inputsColumnIndex] = 'Default'
    cursor.setSheetContent(inputList.sheet, inputList.data)


def generateDefaultInputs(inputList):
    """
    A function that creates an Input List called 'Default' if the Inputs is currently empty.
    """
    if len(inputList.dataRows) == 0:
        length = len(inputList.data[0])
        input1 = helper.createEmptyRow(length)
        input2 = helper.createEmptyRow(length)
        input3 = helper.createEmptyRow(length)
        input4 = helper.createEmptyRow(length)
        input5 = helper.createEmptyRow(length)
        input6 = helper.createEmptyRow(length)

        input1[inputList.nameColumnIndex] = 'Letting go of input'
        input2[inputList.nameColumnIndex] = 'Move'
        input2[inputList.buttonColumnIndex] = 'WASD / L-stick'
        input3[inputList.nameColumnIndex] = 'Jump'
        input3[inputList.buttonColumnIndex] = 'Space / X'
        input4[inputList.nameColumnIndex] = 'Roll'
        input5[inputList.nameColumnIndex] = 'Attack'
        input6[inputList.nameColumnIndex] = 'Block'

        inputList.data.append(input1)
        inputList.data.append(input2)
        inputList.data.append(input3)
        inputList.data.append(input4)
        inputList.data.append(input5)
        inputList.data.append(input6)

        cursor.setSheetContent(inputList.sheet, inputList.data)
