from movelister import loop


def getImpossibleVariations(modifierSheet):
    MDA = getModifierList(modifierSheet)
    XORStartCol = loop.getColumnLocation(modifierSheet, 'XOR Group:')
    XOREndCol = loop.getColumnLocation(modifierSheet, 'AND Group:') - 1
    ANDStartCol = loop.getColumnLocation(modifierSheet, 'AND Group:')
    ANDEndCol = loop.getColumnLocation(modifierSheet, 'Implies:') - 1
    XORAmount = XOREndCol - XORStartCol
    ANDAmount = ANDEndCol - ANDStartCol
    currentGroup = -1
    currentRowGroups = [[], []]
    y = -1

    # A loop starts moving through the Modifier Sheet's XOR groups.
    while y < XORAmount:
        y = y + 1

        x = 0
        while x < len(MDA) - 1:
            x = x + 1
            if MDA[x][XORStartCol + y] != '':
                if currentGroup != MDA[x][XORStartCol + y]:
                    currentGroup = MDA[x][XORStartCol + y]
                    print('new currentGroup is ' + str(currentGroup))

    # To do: this function is supposed to calculate all impossible variations
    # using the rulesets in Modifier sheet. It will also include a single "empty".
    antiVariationSet = {()}
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
