def testItOut(inputSheet, inputsArray):
    x = 1
    while x < len(inputsArray[0]):
        inputSheet.getCellByPosition(8, x).setString(inputsArray[0][x])
        inputSheet.getCellByPosition(9, x).setString(inputsArray[1][x])
        inputSheet.getCellByPosition(10, x).setString(inputsArray[2][x])
        x = x + 1
