def testItOut(inputSheet, inputsArray):

    # The cell range has to be exactly the size of the array or you get a runtime error.
    range = inputSheet.getCellRangeByPosition(11, 1, 13, len(inputsArray))
    range.setDataArray(inputsArray)

    inputSheet.getCellByPosition(15, 2).setString(len(inputsArray))

    # while x < len(inputsArray[0][0]):
    # inputSheet.getCellByPosition(8, x + 1).setString(inputsArray[x][0])
    # inputSheet.getCellByPosition(9, x + 1).setString(inputsArray[x][1])
    # inputSheet.getCellByPosition(10, x + 1).setString(inputsArray[x][2])
    # inputSheet.getCellByPosition(11, x + 1).setString(inputsArray[x][3])
    # x = x + 1
