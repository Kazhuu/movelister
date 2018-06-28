from movelister import cursor, messageBox


def getInputList(inputSheet):
    inputDataArray = cursor.getSheetContent(inputSheet)

    return inputDataArray


def getSpecificInputList(inputSheet, inputGroupName):
    IDA = getInputList(inputSheet)
    x = -1
    startRow = -1
    endRow = -1

    if inputGroupName == '':
        inputGroupName = 'Default'

    for row in IDA:
        x = x + 1
        if row[0] == inputGroupName and startRow == -1:
            startRow = x
        if row[0] != inputGroupName and startRow > -1:
            endRow = x - 1
            break

    if startRow == -1:
        messageBox.createMessage('OK', 'Warning:', 'Program was not able to find a desired input list.')
        exit()

    # The four attributes for CellRangeByPosition are: left, top, right, bottom.
    range = inputSheet.getCellRangeByPosition(1, startRow, 3, endRow)

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


def getSpecificInputListLengths(inputSheet):
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

    return inputListLengths
