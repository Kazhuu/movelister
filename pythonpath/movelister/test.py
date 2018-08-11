def printProjectionTest(projection, masterSheet):
    x = 1

    for zzyy in projection[0]:
        x = x + 1
        zzyyx = str(zzyy)
        masterSheet.getCellByPosition(19, x).setString(zzyyx)
    x = 1
    for zzyy in projection[1]:
        x = x + 1
        zzyyx = str(zzyy)
        masterSheet.getCellByPosition(20, x).setString(zzyyx)
    x = 1
    for zzyy in projection[3]:
        x = x + 1
        zzyyx = str(zzyy)
        masterSheet.getCellByPosition(21, x).setString(zzyyx)


def printMechanicsListTest(projection, mechanicsSheet):
    x = 0

    for zzyy in projection[0]:
        x = x + 1
        zzyyx = str(zzyy)
        mechanicsSheet.getCellByPosition(25, x).setString(zzyyx)
    x = 0
    for zzyy in projection[1]:
        x = x + 1
        zzyyx = str(zzyy)
        mechanicsSheet.getCellByPosition(26, x).setString(zzyyx)
    x = 0
    for zzyy in projection[2]:
        x = x + 1
        zzyyx = str(zzyy)
        mechanicsSheet.getCellByPosition(27, x).setString(zzyyx)


def printModifierListTest(modifierDataArray, modifierListColors, modifierSheet):
    x = 0

    for zzyy in modifierDataArray:
        x = x + 1
        zzyyx = str(zzyy)
        modifierSheet.getCellByPosition(12, x).setString(zzyyx)
    x = 0
    for zzyy in modifierListColors:
        x = x + 1
        zzyyx = str(zzyy)
        modifierSheet.getCellByPosition(13, x).setString(zzyyx)


def testItOut(inputSheet, inputDataArray):

    # The cell range has to be exactly the size of the array or you get a runtime error.
    range = inputSheet.getCellRangeByPosition(11, 1, 13, len(inputDataArray))
    range.setDataArray(inputDataArray)

    inputSheet.getCellByPosition(15, 2).setString(len(inputDataArray))
