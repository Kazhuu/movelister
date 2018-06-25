import itertools

from movelister import cursor, loop


def getModifierList(modifierSheet):
    modifierDataArray = cursor.getSheetContent(modifierSheet)

    return modifierDataArray


def getImpossibleVariations(modifierSheet, mode):
    MDA = getModifierList(modifierSheet)

    if mode == 'OR':  # returned as a multi-dimensional list
        antiVariations = getAntiVariations(MDA, modifierSheet, 'OR')
    if mode == 'NAND':  # returned as a set
        antiVariations = getAntiVariations(MDA, modifierSheet, 'NAND')
    if mode == 'XNOR':  # returned as a 2d-list
        antiVariations = getAntiVariations(MDA, modifierSheet, 'XNOR')
    # TO DO: a code for 'IF' groups. But that isn't a priority yet...

    return antiVariations


def getAntiVariations(MDA, modifierSheet, mode):
    currentRowGroups = [[], [], [], [], [], [], [], [], [], []]
    combinationsList = []
    antiVariationSet = {}

    # Current code supports 10 different rule groups per column.
    # It can be increased by increasing the size of the currentRowGroups array.

    if mode == 'OR':
        ORStartCol = loop.getColumnLocation(modifierSheet, 'OR Group:')
        OREndCol = loop.getColumnLocation(modifierSheet, 'NAND Group:') - 1
        ORAmount = OREndCol - ORStartCol
        loopAmount = ORAmount
        startCol = ORStartCol
        ORList = []
    if mode == 'NAND':
        NANDStartCol = loop.getColumnLocation(modifierSheet, 'NAND Group:')
        NANDEndCol = loop.getColumnLocation(modifierSheet, 'XNOR Group:') - 1
        NANDAmount = NANDEndCol - NANDStartCol
        loopAmount = NANDAmount
        startCol = NANDStartCol
    if mode == 'XNOR':
        XNORList = [[], []]
        XNORStartCol = loop.getColumnLocation(modifierSheet, 'XNOR Group:')
        XNOREndCol = loop.getColumnLocation(modifierSheet, 'IF Group:') - 1
        XNORAmount = XNOREndCol - XNORStartCol
        loopAmount = XNORAmount
        startCol = XNORStartCol

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

        # Iterate through currentRowGroups and calculate all combinations per row if XNOR or NAND.
        # Append the combinations to combinationsList.
        if mode == 'NAND' or mode == 'XNOR':
            combinationsList = iterateCombinations(currentRowGroups, combinationsList, mode)

        if mode == 'XNOR':
            XNORList[0].append(combinationsList[0])
            XNORList[1].append(combinationsList[1])
            combinationsList.clear()

        if mode == 'OR':
            ORList.append(currentRowGroups)

        # Re-initialize values for next column.
        currentRowGroups = [[], [], [], [], [], [], [], [], [], []]

    # Individual numbers are filtered out of the set because those are unaffected
    # by NAND rules. Complex combinations are also filtered out. The list is then
    # made into a set to remove duplicates.
    if mode == 'NAND':
        filterResults = list([x for x in combinationsList if len(x) == 2])
        antiVariationSet = set(filterResults)
        return antiVariationSet

    if mode == 'XNOR':
        return XNORList

    if mode == 'OR':
        return ORList


def iterateCombinations(currentRowGroups, combinationsList, mode):
    tempRow = []
    XNORList = [[], []]

    # Iterate through currentRowGroups and calculate all combinations per index.
    z = -1
    while z < len(currentRowGroups) - 1:
        z = z + 1

        # The code unpacks all values from a single index of currentRowGroups to tempRow.
        zyx = -1
        while zyx < len(currentRowGroups[z]) - 1:
            zyx = zyx + 1
            tempRow.append(currentRowGroups[z][zyx])

        # If there's anything on the tempRow, code calculates all iterations of it.
        if len(tempRow) > 0:
            for L in range(0, len(tempRow) + 1):
                for subset in itertools.combinations(tempRow, L):
                    combinationsList.append(subset)

            # 'XNOR' rules require early filtering inside the loop.
            if mode == 'XNOR':
                XNORList = [[], []]
                filterResults = [x for x in combinationsList if len(x) == len(tempRow)]
                XNORList[1].append(filterResults)

            # Clear variables for next index.
            tempRow.clear()

    if mode == 'NAND':
        return combinationsList

    if mode == 'XNOR':
        filterResults = [x for x in combinationsList if len(x) == 1]
        XNORList[0].append(filterResults)
        return XNORList


def getModifierListColors(modifierSheet, listLength):
    x = 1
    modifierColors = []

    # Iterate through Results List color column to get a list of colors.
    while x < listLength + 1:
        modifierColors.append(modifierSheet.getCellByPosition(2, x).CellBackColor)
        x = x + 1

    return modifierColors
