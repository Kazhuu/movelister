import itertools

from movelister import cursor, error, loop
from movelister.sheet import Sheet


BOOLEAN_AREA_START_COLUMN_NAME = 'Color'
BOOLEAN_AREA_END_COLUMN_NAME = 'Chain'


def getBooleanColumns():
    """
    Function returns boolean columns in two-dimensional array. Columns include
    all user provided boolean columns, not, math and chain columns.
    """
    sheet = Sheet.getModifierSheet()
    startCol = loop.getColumnPosition(sheet, BOOLEAN_AREA_START_COLUMN_NAME) + 1
    endCol = loop.getColumnPosition(sheet, BOOLEAN_AREA_END_COLUMN_NAME)
    return cursor.getColumns(sheet, startCol, endCol)


def getModifierList(modifierSheet):
    modifierDataArray = cursor.getSheetContent(modifierSheet)

    return modifierDataArray


def getModifierListProjection(modifierSheet):
    """
    This function returns a one-dimensional List of all the existing modifiers.
    """
    modifierDataArray = getModifierList(modifierSheet)
    modifierList = []

    x = 0
    for z in modifierDataArray:
        x = x + 1
        if z[0] != '' and x > 1:
            modifierList.append(z[0])

    return modifierList


def getImpossibleVariations(modifierSheet, mode):
    mda = getModifierList(modifierSheet)

    if mode == 'OR':  # returned as a multi-dimensional list
        antiVariations = getAntiVariations(mda, modifierSheet, 'OR')
    if mode == 'NAND':  # returned as a set
        antiVariations = getAntiVariations(mda, modifierSheet, 'NAND')
    if mode == 'XNOR':  # returned as a 2d-list
        antiVariations = getAntiVariations(mda, modifierSheet, 'XNOR')

    # Known bugs: code becomes confused if there is more than one XNOR group.

    return antiVariations


def getAntiVariations(mda, modifierSheet, mode):
    """
    This code calculates all the possible variations that cannot exist because of
    user-set modifier rules. This list is then used to cull down the number of
    variations of a single action to a more manageable size.
    """
    currentRowGroups = [[], [], [], [], [], [], [], [], [], []]
    combinationsList = []
    antiVariationSet = {}

    # Current code supports 10 different rule groups per column.
    # It can be increased by increasing the size of the currentRowGroups array.

    if mode == 'OR':
        ORStartCol = loop.getColumnPosition(modifierSheet, 'OR Group:')
        OREndCol = loop.getColumnPosition(modifierSheet, 'NAND Group:') - 1
        ORAmount = OREndCol - ORStartCol
        loopAmount = ORAmount
        startCol = ORStartCol
        ORList = []
    if mode == 'NAND':
        NANDStartCol = loop.getColumnPosition(modifierSheet, 'NAND Group:')
        NANDEndCol = loop.getColumnPosition(modifierSheet, 'XNOR Group:') - 1
        NANDAmount = NANDEndCol - NANDStartCol
        loopAmount = NANDAmount
        startCol = NANDStartCol
    if mode == 'XNOR':
        XNORList = [[], []]
        XNORStartCol = loop.getColumnPosition(modifierSheet, 'XNOR Group:')
        XNOREndCol = loop.getColumnPosition(modifierSheet, 'Notes 1') - 1
        XNORAmount = XNOREndCol - XNORStartCol
        loopAmount = XNORAmount
        startCol = XNORStartCol

    # A bit of error checking before starting.
    error.impossibleVariationsErrorCheck(mode, loopAmount)

    # A loop starts moving through the Modifier Sheet's columns from left to right..
    y = -1
    while y < loopAmount:
        y = y + 1

        # Another loop starts moving through the rows from up to down.
        x = 0
        while x < len(mda) - 1:
            x = x + 1

            # If there are numbers on a single column, they are appended to their
            # respective index in currentRowGroups.
            if mda[x][startCol + y] != '':
                currentRowGroups[int(mda[x][startCol + y])].append(x)

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
