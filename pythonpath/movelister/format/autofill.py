from movelister.core import cursor
from movelister.sheet import master


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


def autoFillInputs():
    '''
    A function that checks if Input List column is properly filled in Inputs before generating.
    If a row has a Name but no Input List, then the latter field is filled with 'Default'.
    '''
    print()


def generateDefaultInputs():
    '''
    A function that creates an Input List called 'Default' if one doesn't exist in the project
    for a reason or another.
    '''
    print()
