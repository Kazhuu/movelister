def printProjectionTest(projection, masterSheet):
    x = 0

    for zzyy in projection[0]:
        x = x + 1
        zzyyx = str(zzyy)
        masterSheet.getCellByPosition(18, x).setString(zzyyx)
    x = 0
    for zzyy in projection[1]:
        x = x + 1
        zzyyx = str(zzyy)
        masterSheet.getCellByPosition(19, x).setString(zzyyx)
    x = 0

    for zzyy in projection[2]:
        x = x + 1
        zzyyx = str(zzyy)
        masterSheet.getCellByPosition(20, x).setString(zzyyx)


def testItOut(inputSheet, inputDataArray):

    # The cell range has to be exactly the size of the array or you get a runtime error.
    range = inputSheet.getCellRangeByPosition(11, 1, 13, len(inputDataArray))
    range.setDataArray(inputDataArray)

    inputSheet.getCellByPosition(15, 2).setString(len(inputDataArray))
