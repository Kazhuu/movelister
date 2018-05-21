def testItOut(inputSheet, inputDataArray):

    # The cell range has to be exactly the size of the array or you get a runtime error.
    range = inputSheet.getCellRangeByPosition(11, 1, 13, len(inputDataArray))
    range.setDataArray(inputDataArray)

    inputSheet.getCellByPosition(15, 2).setString(len(inputDataArray))

    # while x < len(inputDataArray[0][0]):
    # inputSheet.getCellByPosition(8, x + 1).setString(inputDataArray[x][0])
    # inputSheet.getCellByPosition(9, x + 1).setString(inputDataArray[x][1])
    # inputSheet.getCellByPosition(10, x + 1).setString(inputDataArray[x][2])
    # inputSheet.getCellByPosition(11, x + 1).setString(inputDataArray[x][3])
    # x = x + 1
