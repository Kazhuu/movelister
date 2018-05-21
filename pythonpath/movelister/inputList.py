def getInputList(inputSheet, inputGroupName):
    x = 1
    startRow = -1
    endRow = -1

    # The loop iterates through a desired input list to find its coordinates.
    # The loop breaks once there are two blank rows in the list.
    while True:
        if inputSheet.getCellByPosition(0, x).getString() == inputGroupName:
                if startRow == -1:
                    startRow = x
                if inputSheet.getCellByPosition(0, x + 1).getString() == "":
                    endRow = x
        if inputSheet.getCellByPosition(0, x).getString() == "":
            if inputSheet.getCellByPosition(0, x + 1).getString() == "":
                break
        x = x + 1

    inputSheet.getCellByPosition(11, 5).setString(startRow)
    inputSheet.getCellByPosition(11, 6).setString(endRow)
    range = inputSheet.getCellRangeByPosition(1, startRow, 3, endRow)

    inputsArray = range.getDataArray()
    return inputsArray
