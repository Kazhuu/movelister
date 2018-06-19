import itertools

from movelister import loop


def getImpossibleVariations(modifierSheet):
    MDA = getModifierList(modifierSheet)
    XORStartCol = loop.getColumnLocation(modifierSheet, 'XOR Group:')
    XOREndCol = loop.getColumnLocation(modifierSheet, 'AND Group:') - 1
    ANDStartCol = loop.getColumnLocation(modifierSheet, 'AND Group:')
    ANDEndCol = loop.getColumnLocation(modifierSheet, 'IF Group:') - 1
    XORAmount = XOREndCol - XORStartCol
    ANDAmount = ANDEndCol - ANDStartCol
    totalColumns = XORAmount + ANDAmount
    totalLoopCount = 0
    currentRowGroups = [[], [], [], [], [], [], [], [], [], []]
    tempList = []
    combinationsList = []
    y = -1

    # Current code supports 10 different rule groups per column.
    # It can be increased by increasing the size of the currentRowGroups array.

    # A loop starts moving through the Modifier Sheet's XOR columns from left to right..
    while y < XORAmount:
        y = y + 1

        # Another loop starts moving through the rows from up to down.
        x = 0
        while x < len(MDA) - 1:
            x = x + 1

            # If there are numbers on a single column, they are appended to their
            # respective index on currentRowGroups.
            if MDA[x][XORStartCol + y] != '':
                currentRowGroups[int(MDA[x][XORStartCol + y])].append(x)

        # Iterate through currentRowGroups and calculate all combinations per row.
        # Append the combinations to combinationsList.
        tempList = iterateCombinations(currentRowGroups, combinationsList)
        combinationsList = tempList

        # Re-initialize values for next column.
        currentRowGroups = [[], [], [], [], [], [], [], [], [], []]
        totalLoopCount = totalLoopCount + 1

    # To do: implement AND groups.

    # Individual numbers are filtered out of the set because those are unaffected
    # by XOR rules. Complex combinations are also filtered out. The list is then
    # made into a set to remove duplicates.
    filteredList = [x for x in combinationsList if len(x) == 2]
    antiVariationSet = set(filteredList)

    return antiVariationSet


def iterateCombinations(currentRowGroups, combinationsList):
    tempRow = []
    z = -1

    # Iterate through currentRowGroups and calculate all combinations per row.
    while z < len(currentRowGroups) - 1:
        z = z + 1
        tempIndex = -1
        while tempIndex < len(currentRowGroups[z]) - 1:
            tempIndex = tempIndex + 1
            tempRow.append(currentRowGroups[z][tempIndex])

        if len(tempRow) > 0:
            for L in range(0, len(tempRow) + 1):
                for subset in itertools.combinations(tempRow, L):
                    combinationsList.append(subset)
            tempRow.clear()

    return combinationsList


def getModifierList(modifierSheet):
    endRow = -1
    rulesEndCol = loop.getColumnLocation(modifierSheet, 'Notes 1:') - 1

    # The loop iterates through Modifier List to get its end row.
    # The loop breaks once there are two empty rows or x is over 1000.
    endRow = loop.getEndOfList(modifierSheet)

    # The four attributes for CellRangeByPosition are: left, top, right, bottom.
    # The array is wide enough to get ALL relevant rules information too.
    range = modifierSheet.getCellRangeByPosition(0, 0, rulesEndCol, endRow + 1)

    modifierDataArray = range.getDataArray()
    return modifierDataArray


def getModifierListColors(modifierSheet, listLength):
    x = 1
    modifierColors = []

    # Iterate through Results List color column to get a list of colors.
    while x < listLength + 1:
        modifierColors.append(modifierSheet.getCellByPosition(2, x).CellBackColor)
        x = x + 1

    return modifierColors
