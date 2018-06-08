import itertools

from movelister import loop, messageBox, modifierList


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
    MDA = getMasterList(masterSheet)
    nameCol = loop.getColumnLocation(masterSheet, 'Action Name')
    modStartCol = loop.getColumnLocation(masterSheet, 'DEF')
    modEndCol = loop.getColumnLocation(masterSheet, 'Full Name') - 1
    modAmount = modEndCol - modStartCol
    currentName = MDA[1][nameCol]
    currentActionRow = -1
    totalActions = 0
    projection = [[], []]
    tempString = ''
    tempProjection = [[], []]
    currentActionDEF = -1
    currentActionMods = [[], []]
    currentActionMods.clear()
    currentPrereqs = ''
    prereqsDone = -1
    x = 0

    # A bit of error checking.
    if len(MDA) <= 2 and MDA[1][nameCol] == '':
        messageBox.createMessage('OK', 'Warning:', 'Master Action List seems to be empty. Unable to generate.')
        exit()

    # Get an array of impossible variations (derived from Modifier rules) to compare with the action list later on.
    antiVariationSet = modifierList.getImpossibleVariations(modifierSheet)

    # Loop through rows of Master Action List (represented as the multi-dimensional List MDA).
    while x < len(MDA) - 1:
        x = x + 1
        currentActionRow = currentActionRow + 1

        # currentActionMods has to be appended each row so that it has space for listing all the 'X'
        # per each row of the animation.
        currentActionMods.append([])

        # Loop through columns to make a string of potential 'P' (prerequisites) markings.
        if prereqsDone == -1:
            y = -1
            while y < modAmount:
                y = y + 1

                # If a column has 'P' in any spot past 'DEF' column, it's recorded to be used as a string.
                # The variable prereqsDone is used to prevent initializing multiple times per animation.
                # if (currentActionRow == 0 and len(currentActionMods) <= 1) or currentActionRow > 0:
                if MDA[x - 1][modStartCol + y] == 'P' and y > 0:
                    prereqsDone == 0
                    if currentPrereqs != '':
                        currentPrereqs = currentPrereqs + ' + ' + MDA[0][modStartCol + y]
                    else:
                        currentPrereqs = currentPrereqs + MDA[0][modStartCol + y]
                    print('currentPrereqs was changed to ' + currentPrereqs)

        # Loop for going through all modifier columns.
        if currentName == MDA[x][nameCol]:
            y = -1
            while y < modAmount:
                y = y + 1

                # If first column (DEF) has 'X' and tempProjection is empty, the code acknowledges
                # that there needs to be a modifier-less default variation of the action.
                if MDA[x][modStartCol + y] == 'X' and y == 0 and currentActionDEF < 1:
                    currentActionDEF = 1
                    print('There will be a DEF version of ' + currentName)

                    # If a column has 'X' in any other circumstance...
                    # Collect all the 'X' for each row in a multi-dimensional array currentActionMods.
                if MDA[x][modStartCol + y] == 'X' and y > 0:
                    currentActionMods[currentActionRow].append(y)

        # If currentName doesn't match current row, update it. This signifies the start of a new action.
        if currentName != MDA[x][nameCol]:

            # Process the currentActionMods list to figure out all the possible variations of the action.
            # The procession happens row by row because otherwise some variations will be missed.
            if len(currentActionMods) > 1:
                print('currentActionMods ' + str(currentActionMods))

                # Get a set of all possible variations of a single action.
                variationSet = getPossibleVariations(currentActionMods)

                # Delete impossible combinations (and blanks) from the set based on modifier rules.
                realisticSet = (variationSet - antiVariationSet)

                # Sort the set.
                sortedSet = sorted(realisticSet)

                if currentActionDEF == 1:
                    tempProjection[0].append(currentName)
                    tempProjection[1].append(currentPrereqs)

                if len(sortedSet) > 0:
                    print('All combinations of ' + currentName + ': ' + str(sortedSet))

                    # Adding the animations in the tempProjection.
                    for xx in sortedSet:
                        for xxy in xx:
                            if tempString == '':
                                tempString = tempString + MDA[0][modStartCol + xxy]
                            else:
                                tempString = tempString + ' + ' + MDA[0][modStartCol + xxy]

                        tempProjection[0].append(currentName)
                        if currentPrereqs != '' and tempString != '':
                            tempProjection[1].append(currentPrereqs + ' + ' + tempString)
                        elif currentPrereqs != '' and tempString == '':
                            tempProjection[1].append(currentPrereqs)
                        else:
                            tempProjection[1].append(tempString)
                            tempString = ''

                # Add all content from tempProjection into final projection data array.
                xyx = -1
                while xyx < len(tempProjection) - 1:
                    xyx = xyx + 1
                    for o in tempProjection[xyx]:
                        projection[xyx].append(o)

            # Update currentName with new action and re-initialize variables for next action.
            currentName = MDA[x][nameCol]
            print("name updated to " + currentName)
            currentActionRow = -1
            currentActionMods.clear()
            tempProjection = [[], []]
            tempString = ''
            currentPrereqs = ''
            prereqsDone = -1
            currentActionDEF = -1
            x = x - 1

            # Add to the variable that tells how many actions the code has listed so far.
            totalActions = totalActions + 1

    # A quick test that prints out the contents of the projection.
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


def getPossibleVariations(currentActionMods):
    z = -1
    tempMods1 = []
    tempMods2 = []

    # The loop unpacks all values from currentActionMods to tempMods2.
    # Then calculates and appends all combinations of those values to tempMods1.
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

    # Converts tempMods1 into a set to delete all duplicates.
    tempSet = set(tempMods1)
    return tempSet


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
