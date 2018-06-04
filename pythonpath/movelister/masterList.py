import itertools

from movelister import loop, messageBox


def getMasterList(masterSheet):
    endRow = -1
    modEndCol = loop.getColumnLocation(masterSheet, 'Full Name') - 1

    # The loop iterates through Master Action List to get its end row.
    # The loop breaks once there are two empty rows or x is over 1000.
    endRow = loop.getEndOfList(masterSheet)

    # The four attributes for CellRangeByPosition are: left, top, right, bottom.
    # The data array consists of ALL relevant data in the sheet, including modifiers.
    range = masterSheet.getCellRangeByPosition(0, 0, modEndCol, endRow + 1)

    masterDataArray = range.getDataArray()
    return masterDataArray


def getMasterListProjection(masterSheet, modifierSheet):
    nameCol = loop.getColumnLocation(masterSheet, 'Action Name')
    phaseCol = loop.getColumnLocation(masterSheet, 'Phase')
    modStartCol = loop.getColumnLocation(masterSheet, 'DEF')
    modEndCol = loop.getColumnLocation(masterSheet, 'Full Name') - 1
    modAmount = modEndCol - modStartCol
    currentName = 'zzzxxx'
    currentActionRow = -1
    totalActions = 0
    projection = [[], []]
    tempString = ''
    tempList = [[], []]
    tempSet = {}
    tempMods1 = []
    tempMods2 = []
    currentActionMods = [[], []]
    currentActionMods.clear()
    currentPrereqs = ''
    prereqsDone = -1
    x = 0
    MDA = getMasterList(masterSheet)

    # A bit of error checking.
    if len(MDA) <= 1:
        messageBox.createMessage("OK", "Warning:", "Master Action List seems to be empty. Unable to generate.")
        exit()

    # Loop through rows of Master Action List (represented as the multi-dimensional List MDA).
    while x < len(MDA) - 1:
        x = x + 1
        currentActionRow = currentActionRow + 1

        # If currentName doesn't match current row, update it.
        if currentName != MDA[x][nameCol]:

            # Process the currentActionMods list to figure out all the possible variations of the action.
            # The procession happens row by row because otherwise some variations will be missed.
            # No need to do this on the first loop of the code.
            if totalActions > 0:
                if len(currentActionMods) > 1:
                    z = -1
                    tempMods1.clear()

                    # Unpacks all value combinations from a single row of currentActionMods to tempMods1.
                    while z < len(currentActionMods) - 1:
                        tempMods2.clear()
                        z = z + 1
                        xyz = -1
                        while xyz < len(currentActionMods[z]) - 1:
                            xyz = xyz + 1
                            tempMods2.append(currentActionMods[z][xyz])
                            if len(tempMods2) > 0:
                                for L in range(0, len(tempMods2) + 1):
                                    for subset in itertools.combinations(tempMods2, L):
                                        tempMods1.append(subset)

                    # After all variations per row calculated and appended into tempMods1, the data is made
                    # into a set so that duplicates are removed.
                    tempSet = set(tempMods1)

                    # Delete impossible combinations from the tempSet based on the modifier rules.
                    # Also delete blank entries.

                    # Sort tempSet.
                    sortedSet = sorted(tempSet)
                    print(sortedSet)

                    # Adding the animations in the tempList.
                    z = -1
                    for xx in sortedSet:
                        for xxy in xx:
                            if tempString == '':
                                tempString = tempString + MDA[0][modStartCol + xxy]
                            else:
                                tempString = tempString + ' + ' + MDA[0][modStartCol + xxy]

                        tempList[0].append(currentName)
                        if currentPrereqs != '' and tempString != '':
                            tempList[1].append(currentPrereqs + ' + ' + tempString)
                        elif currentPrereqs != '' and tempString == '':
                            tempList[1].append(currentPrereqs)
                        else:
                            tempList[1].append(tempString)
                        tempString = ''

            # Add all content from tempList into final projection data array.
            xyx = -1
            while xyx < len(tempList) - 1:
                xyx = xyx + 1
                for o in tempList[xyx]:
                    projection[xyx].append(o)

            # Update currentName with new action and re-initialize variables for next action.
            currentName = MDA[x][nameCol]
            currentActionRow = 0
            currentActionMods.clear()
            tempSet.clear()
            tempList = [[], []]
            currentPrereqs = ''
            prereqsDone = -1

            # Add to the variable that tells how many actions the code has listed so far.
            totalActions = totalActions + 1

        # currentActionMods has to be appended each row so that it has space for listing all the 'X'
        # per each row of the animation.
        currentActionMods.append([])

        # Loop for going through columns.
        y = -1
        while y < modAmount:
            y = y + 1

            # If first (DEF) column has 'X' and tempList is empty, the default version of an action
            # can be safely added to tempList.
            if MDA[x][modStartCol + y] == 'X' and y == 0 and len(tempList[0]) == 0:
                tempList[0].append(currentName)
                tempList[1].append('')

            # If a column has 'X' in any other circumstance...
            # Collect all the 'X' for each row in a multi-dimensional array currentActionMods.
            if MDA[x][modStartCol + y] == 'X' and y > 0:
                    currentActionMods[currentActionRow].append(y)

        # Second loop through columns to handle 'P' (prerequisites).
        y = -1
        while y < modAmount:
            y = y + 1

            # If a column has 'P' in any spot past 'DEF' column, it's recorded to be used as a string.
            # The variable prereqsDone is used to prevent initializing multiple times per animation.
            # If an action has more than 1 phase, the first line of the action is ignored.
            if prereqsDone == -1:
                if (currentActionRow == 0 and len(currentActionMods) <= 1) or currentActionRow > 0:
                    if MDA[x][modStartCol + y] == 'P' and y > 0:
                        prereqsDone == 0
                        if currentPrereqs != '':
                            currentPrereqs = currentPrereqs + ' + ' + MDA[0][modStartCol + y]
                        else:
                            currentPrereqs = currentPrereqs + MDA[0][modStartCol + y]

        # Re-initialize values for next loop.
        y = -1

    # A quick test that prints out the contents of the projection.
    x = 0
    for zzyy in projection[0]:
        x = x + 1
        zzyyx = str(zzyy)
        masterSheet.getCellByPosition(14, x).setString(zzyyx)
    x = 0
    for zzyy in projection[1]:
        x = x + 1
        zzyyx = str(zzyy)
        masterSheet.getCellByPosition(15, x).setString(zzyyx)


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
