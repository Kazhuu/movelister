import itertools

from movelister import loop


def getImpossibleVariations(modifierSheet, mode):
    MDA = getModifierList(modifierSheet)

    if mode == 'XOR':  # returned as a set
        antiVariations = getAntiVariations(MDA, modifierSheet, 'XOR')
    if mode == 'AND':  # returned as a 2d-list
        antiVariations = getAntiVariations(MDA, modifierSheet, 'AND')
    # TO DO: a code for 'IF' groups. But that isn't a priority yet...

    return antiVariations


def getAntiVariations(MDA, modifierSheet, mode):
    currentRowGroups = [[], [], [], [], [], [], [], [], [], []]
    combinationsList = []

    # Current code supports 10 different rule groups per column.
    # It can be increased by increasing the size of the currentRowGroups array.

    if mode == 'XOR':
        XORStartCol = loop.getColumnLocation(modifierSheet, 'XOR Group:')
        XOREndCol = loop.getColumnLocation(modifierSheet, 'AND Group:') - 1
        XORAmount = XOREndCol - XORStartCol
        loopAmount = XORAmount
        startCol = XORStartCol
    if mode == 'AND':
        completeList = [[], []]
        ANDStartCol = loop.getColumnLocation(modifierSheet, 'AND Group:')
        ANDEndCol = loop.getColumnLocation(modifierSheet, 'IF Group:') - 1
        ANDAmount = ANDEndCol - ANDStartCol
        loopAmount = ANDAmount
        startCol = ANDStartCol

    # A loop starts moving through the Modifier Sheet's columns from left to right..
    y = -1
    while y < loopAmount:
        y = y + 1

        # Another loop starts moving through the rows from up to down.
        x = 0
        while x < len(MDA) - 1:
            x = x + 1

            # If there are numbers on a single column, they are appended to their
            # respective index in currentRowGroups.
            if MDA[x][startCol + y] != '':
                currentRowGroups[int(MDA[x][startCol + y])].append(x)

        # Iterate through currentRowGroups and calculate all combinations per row.
        # Append the combinations to combinationsList.
        combinationsList = iterateCombinations(currentRowGroups, combinationsList, mode)

        if mode == 'AND':
            completeList[0].append(combinationsList[0])
            completeList[1].append(combinationsList[1])
            combinationsList.clear()

        # Re-initialize values for next column.
        currentRowGroups = [[], [], [], [], [], [], [], [], [], []]

    # Individual numbers are filtered out of the set because those are unaffected
    # by XOR rules. Complex combinations are also filtered out. The list is then
    # made into a set to remove duplicates.
    if mode == 'XOR':
        filterResults = list([x for x in combinationsList if len(x) == 2])
        antiVariationSet = set(filterResults)

    if mode == 'AND':
        return completeList

    return antiVariationSet


def iterateCombinations(currentRowGroups, combinationsList, mode):
    tempRow = []
    z = -1
    completeList = [[], []]

    # Iterate through currentRowGroups and calculate all combinations per index.
    while z < len(currentRowGroups) - 1:
        z = z + 1

        # The code unpacks all values from a single index of currentRowGroups to tempRow.
        tempIndex = -1
        while tempIndex < len(currentRowGroups[z]) - 1:
            tempIndex = tempIndex + 1
            tempRow.append(currentRowGroups[z][tempIndex])

        # If there's anything on the tempRow, code calculates all iterations of it.
        if len(tempRow) > 0:
            for L in range(0, len(tempRow) + 1):
                for subset in itertools.combinations(tempRow, L):
                    combinationsList.append(subset)

            # 'AND' rules require early filtering inside the loop.
            if mode == 'AND':
                completeList = [[], []]
                filterResults = [x for x in combinationsList if len(x) == len(tempRow)]
                completeList[1].append(filterResults)
                print(completeList[1])

            # Clear variables for next index.
            tempRow.clear()

    if mode == 'XOR':
        return combinationsList

    if mode == 'AND':
        filterResults = [x for x in combinationsList if len(x) == 1]
        completeList[0].append(filterResults)
        return completeList


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
