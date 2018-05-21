def generateActionFull(mechanicsSheet, inputDataArray, nameField1, nameField2, startRow):

    # Generate empty rows according to Input List length.
    mechanicsSheet.Rows.insertByIndex(startRow, len(inputDataArray))

    inputList, inputColors, inputGroups = zip(*inputDataArray)

    range = mechanicsSheet.getCellRangeByPosition(2, 2, 3, len(inputList))
    # range.setDataArray(inputList)

    # inputSheet.getCellByPosition(15, 2).setString(len(inputDataArray))
    #
    x = 0

    # while x < len(A):
    # mechanicsSheet.getCellByPosition(8, x + 1).setString(A[x])
    # inputSheet.getCellByPosition(9, x + 1).setString(inputDataArray[x][1])
    # inputSheet.getCellByPosition(10, x + 1).setString(inputDataArray[x][2])
    # inputSheet.getCellByPosition(11, x + 1).setString(inputDataArray[x][3])
    # x = x + 1
