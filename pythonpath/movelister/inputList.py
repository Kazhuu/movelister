from movelister import cursor


def getInputList(inputSheet, inputGroupName):
    x = 1
    startRow = 0
    endRow = 0

    if inputGroupName == '':
        inputGroupName = 'Default'

    # The loop iterates through a desired input list to get its coordinates.
    # The loop breaks once there are two non-relevant rows or x is over 1000.
    while x < 1000:
        x = x + 1
        if inputSheet.getCellByPosition(0, x).getString() == inputGroupName:
                if startRow == -1:
                    startRow = x
                if inputSheet.getCellByPosition(0, x + 1).getString() != inputGroupName:
                    endRow = x
                    if inputSheet.getCellByPosition(0, x + 2).getString() != inputGroupName:
                        break

    # The four attributes for CellRangeByPosition are: left, top, right, bottom.
    range = inputSheet.getCellRangeByPosition(1, startRow, 3, endRow + 1)

    inputDataArray = range.getDataArray()
    return inputDataArray


def getInputColors(inputSheet, listLength):
    x = 1
    inputColors = []

    # Iterate through Results List second column to get a list of colors.
    while x < listLength + 1:
        inputColors.append(inputSheet.getCellByPosition(4, x).CellBackColor)
        x = x + 1

    return inputColors


def getInputListLengths(inputSheet):
    IDA = cursor.getSheetContent(inputSheet)
    currentInputList = IDA[1][0]
    inputListLengths = [[], []]

    # Code that calculates the length of all input lists.
    z = 0
    number = 0
    for row in IDA:
        z = z + 1
        if row[0] != currentInputList and z > 1:
            inputListLengths[0].append(currentInputList)
            inputListLengths[1].append(number)
            currentInputList = IDA[z][0]
            number = 0
        if row[0] == currentInputList:
            number = number + 1

    # The last append happens necessarily outside loop.
    if currentInputList != '':
        inputListLengths[0].append(currentInputList)
        inputListLengths[1].append(number)

    inputListLengths[0].append('')
    inputListLengths[0].append('')

    return inputListLengths
