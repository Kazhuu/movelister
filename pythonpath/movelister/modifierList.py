import itertools

from movelister import loop


def getImpossibleVariations(modifierSheet):
    MDA = getModifierList(modifierSheet)
    XORStartCol = loop.getColumnLocation(modifierSheet, 'XOR Group:')
    XOREndCol = loop.getColumnLocation(modifierSheet, 'AND Group:') - 1
    ANDStartCol = loop.getColumnLocation(modifierSheet, 'AND Group:')
    ANDEndCol = loop.getColumnLocation(modifierSheet, 'Implies:') - 1
    XORAmount = XOREndCol - XORStartCol
    ANDAmount = ANDEndCol - ANDStartCol
    tempRow = []
    currentRowGroups = [[], [], [], [], [], [], [], [], [], []]
    tempList = []
    combinationsList = []
    y = -1

    # Current code supports 10 different rule groups per column.
    # It shouldn't be too hard to change, though.

    # A loop starts moving through the Modifier Sheet's XOR columns..
    while y < XORAmount:
        y = y + 1

        # Another loop starts moving through the rows.
        x = 0
        while x < len(MDA) - 1:
            x = x + 1

            # If there is a number on one of the XOR columns, append to that index
            # in currentRowGroups.
            if MDA[x][XORStartCol + y] != '':
                currentRowGroups[int(MDA[x][XORStartCol + y])].append(x)

        # Iterate through currentRowGroups and calculate all combinations.
        # Append the combinations to combinationsList.
        z = -1
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

        # Re-initialize values for next column.
        currentRowGroups = [[], [], [], [], [], [], [], [], [], []]

    # To do: implement AND groups.

    # Individual numbers are filtered out of the set because those are unaffected
    # by XOR rules. Complex combinations are also filtered out. The list is then
    # made into a set to remove duplicates.
    filteredList = [x for x in combinationsList if len(x) == 2]
    antiVariationSet = set(filteredList)

    return antiVariationSet


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
