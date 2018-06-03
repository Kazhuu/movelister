from movelister import loop, messageBox


def getMasterList(masterSheet):
    endRow = -1
    modEndCol = loop.getColumnLocation(masterSheet, 'Full Name') - 1

    # The loop iterates through Master Action List to get its end row.
    # The loop breaks once there are two empty rows or x is over 1000.
    endRow = loop.getEndOfList(masterSheet)

    # The four attributes for CellRangeByPosition are: left, top, right, bottom.
    # To do: the wideness of this array isn't well defined yet. It depends on
    # what's all the data that's actually needed elsewhere.
    range = masterSheet.getCellRangeByPosition(0, 0, modEndCol, endRow)

    masterDataArray = range.getDataArray()
    return masterDataArray


def getMasterListProjection(masterSheet, modifierSheet):
    nameCol = loop.getColumnLocation(masterSheet, 'Action Name')
    phaseCol = loop.getColumnLocation(masterSheet, 'Phase')
    modStartCol = loop.getColumnLocation(masterSheet, 'DEF')
    modEndCol = loop.getColumnLocation(masterSheet, 'Full Name') - 1
    modAmount = modEndCol - modStartCol
    currentName = 'zzzxxx'
    projection = [[],[]]
    tempList = [[],[]]
    tempMods = [[],[]]
    currentPrereqs = ''
    x = 0
    y = -1

    MDA = getMasterList(masterSheet)

    # Loop through rows of Master Action List (represented as the multi-dimensional List MDA).
    while x < len(MDA) - 1:
        x = x + 1
        print(x)

        # If currentName doesn't match current row, update it.
        if currentName != MDA[x][nameCol]:
            currentName = MDA[x][nameCol]

            # Code for getting Prerequisites from the modifier columns.
            # The code makes sure this isn't Phase 0 IF this is an action with more than 0 phases,
            # because using Phase 0 modifiers for the full animation may be misleading.
            tempCol = 0
            tempRow = x
            if MDA[x][phaseCol] < 1 and MDA[x + 1][nameCol] == currentName:
                tempRow = tempRow + 1
            while tempCol < modAmount:
                tempCol = tempCol + 1
                if MDA[tempRow][modStartCol + tempCol] == 'P':
                    if currentPrereqs != '':
                        currentPrereqs = currentPrereqs + ' + ' + MDA[0][modStartCol + tempCol]
                    else:
                        currentPrereqs = currentPrereqs + MDA[0][modStartCol + tempCol]

        # Loop for going through columns.
        while y < modAmount:
            y = y + 1

            # If first (DEF) column has "X" and tempList is empty, the default version of an action
            # can be safely added to tempList.
            if MDA[x][modStartCol + y] == 'X' and y == 0 and len(tempList[0]) == 0:
                tempList[0].append(currentName)
                tempList[1].append(currentPrereqs)
                print(tempList)

            # If a column has X in any other circumstance...
            # Figure out the name of the Mod that is checked.
            # Compare to see if the action name + mod name already exists in the tempList.
            if MDA[x][modStartCol + y] == 'X' and y > 0:

                if len(tempList) > 0:
                    z = -1
                    while z < len(tempList) - 1:
                        z = z + 1
                        print("ohhoh")
                    # if tempList[0][z] == currentName and tempList[1][z] == (currentPrereqs + MDA[0][modStartCol + y]):
                    #     print("ohhoh!")

        # Re-initialize values for next loop.
        y = -1


def getHighestPhaseNumber(masterSheet, listLength):
    x = -1
    phase = 0
    phaseCol = loop.getColumnLocation(masterSheet, 'Phase')

    # The loop iterates through the Phase column and finds the highest number in sequence.
    # Warning: loop cannot find high phase numbers that are out of sequence.
    # But something like that shouldn't happen in normal use, right?
    # Warning: the loop also doesn't check if the high phase numbers are actually in use,
    # (as indicated by the Modifiers columns) so it doesn't do everything it's supposed to yet.
    while x <= listLength:
        x = x + 1
        if masterSheet.getCellByPosition(phaseCol, x).getValue() == phase:
            phase = phase + 1
            x = -1

    return(phase)


def fixModifiers(masterSheet, modifierDataArray):
    print("TO DO")
