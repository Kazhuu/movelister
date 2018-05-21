def getInputList(inputSheet, inputGroupName):
    x = 1
    startRow = -1
    endRow = -1

    # The loop iterates through a desired input list to get its coordinates.
    # The loop breaks once there are two non-relevant rows or x is over 1000.
    while x < 1000:
        if inputSheet.getCellByPosition(0, x).getString() == inputGroupName:
                if startRow == -1:
                    startRow = x
                if inputSheet.getCellByPosition(0, x + 1).getString() != inputGroupName:
                    endRow = x
                    if inputSheet.getCellByPosition(0, x + 2).getString() != inputGroupName:
                        break
        x = x + 1

    inputSheet.getCellByPosition(11, 5).setString(startRow)
    inputSheet.getCellByPosition(11, 6).setString(endRow)
    range = inputSheet.getCellRangeByPosition(1, startRow, 3, endRow)

    inputsArray = range.getDataArray()
    return inputsArray
