import itertools

from movelister import error, inputList, loop, modifierList, test


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


def getMasterListProjection(masterSheet, modifierSheet, inputSheet):
    MDA = getMasterList(masterSheet)
    nameCol = loop.getColumnLocation(masterSheet, 'Action Name')
    modStartCol = loop.getColumnLocation(masterSheet, 'DEF')
    modEndCol = loop.getColumnLocation(masterSheet, 'Full Name') - 1
    modAmount = modEndCol - modStartCol
    currentName = MDA[1][nameCol]
    currentInputList = MDA[1][nameCol - 1]
    currentActionRow = -1
    projection = [[], [], [], []]
    currentActionDEF = -1
    currentActionMods = [[], []]
    currentActionMods.clear()
    currentActionPrereqs = []
    prereqsString = ''

    # A bit of error checking before starting.
    error.masterListProjectionErrorCheck(MDA, nameCol)

    # Get an array of impossible variations (derived from Modifier rules) to compare with the action list later on.
    antiVariationOR = modifierList.getImpossibleVariations(modifierSheet, 'OR')
    antiVariationNAND = modifierList.getImpossibleVariations(modifierSheet, 'NAND')
    antiVariationXNOR = modifierList.getImpossibleVariations(modifierSheet, 'XNOR')
    print('List of OR-rules: ' + str(antiVariationOR))
    print('All impossible variations based on NAND-rules: ' + str(antiVariationNAND))
    print('All impossible variations based on XNOR-rules: ' + str(antiVariationXNOR[0]))
    print('Protected variations (XNOR): ' + str(antiVariationXNOR[1]))

    # Loop through rows of Master Action List (represented as the multi-dimensional List MDA).
    x = 0
    while x < len(MDA) - 1:
        x = x + 1
        currentActionRow = currentActionRow + 1

        # currentActionMods has to be appended each row so that it has space for listing all the 'x'
        # per each row of the animation.
        currentActionMods.append([])

        # Loop for going through all modifier columns.
        if currentName == MDA[x][nameCol]:
            y = -1
            while y < modAmount:
                y = y + 1

                # If first column (DEF) has 'x', there needs to be a modifier-less default version of the action.
                if MDA[x][modStartCol + y] == 'x' and y == 0 and currentActionDEF < 1:
                    currentActionDEF = 1
                    print('There will be a DEF version of ' + currentName)

                # If a column has 'x' in any other circumstance...
                # Collect all the 'x' for each row in a multi-dimensional array currentActionMods.
                if MDA[x][modStartCol + y] == 'x' and y > 0:
                    currentActionMods[currentActionRow].append(y)

                # If a cell has 'P' (prerequisite), store it for now.
                if MDA[x][modStartCol + y] == 'P' and y > 0:
                    currentActionPrereqs.append(MDA[0][modStartCol + y])

        # If currentName doesn't match current row, update it. This signifies the start of a new action.
        if currentName != MDA[x][nameCol]:

            # Make a string out of currentActionPrereqs if needed.
            if len(currentActionPrereqs) > 0:
                prereqsString = makePrereqsString(currentActionPrereqs, prereqsString)

            # Process the currentActionMods list to figure out all the possible variations of the action.
            # The procession happens row by row because otherwise some variations will be missed.
            if len(currentActionMods) > 1:
                sortedList = processVariations(currentActionMods, antiVariationOR, antiVariationNAND,
                                               antiVariationXNOR)

                if currentActionDEF == 1:
                    projection[0].append(currentName)
                    projection[1].append(prereqsString)
                    projection[2].append(currentInputList)

                if len(sortedList) > 0:
                    print('The final list of combinations from ' + currentName + ': ' + str(sortedList))

                    # Add all the variations of the current attack in the projection.
                    projection = fillProjection(MDA, sortedList, projection, currentName, currentInputList,
                                                prereqsString, modStartCol)

            # Update currentName with new action and re-initialize variables for next action.
            currentName = MDA[x][nameCol]
            currentInputList = MDA[x][nameCol - 1]
            print('Next attack is ' + currentName)
            currentActionRow = -1
            currentActionMods.clear()
            currentActionPrereqs = []
            prereqsString = ''
            currentActionDEF = -1
            x = x - 1

    # Estimate the position of each action in Mechanics List.
    projection = estimateActionPositionsForProjection(inputSheet, projection)

    # A quick test that prints out the contents of the projection.
    test.printProjectionTest(projection, masterSheet)

    return projection


def estimateActionPositionsForProjection(inputSheet, projection):

    # Get lengths of all input lists.
    inputListLengths = inputList.getInputListLengths(inputSheet)

    # Code that estimates the position of each action based on input list length.
    # This is added to 'projection' index 4.
    currentPos = 2
    projection[3].append(currentPos)

    z = -1
    while z < len(projection[2]) - 1:
        z = z + 1
        currentInputList = projection[2][z]

        x = -1
        while x < len(inputListLengths) - 1:
            x = x + 1
            if inputListLengths[0][x] == currentInputList:
                currentPos = currentPos + inputListLengths[1][x] + 1
                projection[3].append(currentPos)

    return projection


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


def processVariations(currentActionMods, antiVariationOR, antiVariationNAND, antiVariationXNOR):

    # Get a set of all possible variations of a single action.
    variationSet = getPossibleVariations(currentActionMods)

    # Delete impossible variations from the set based on NAND modifier rules.
    filteredSet1 = processNANDVariations(variationSet, antiVariationNAND)

    # Delete impossible variations from the set based on XNOR modifier rules.
    # TO DO: the code is confused if the project has more than 1 XNOR group. Should be fixed.
    filteredSet2 = processXNORVariations(filteredSet1, antiVariationXNOR)

    # Delete impossible variations from the set based on OR rules.
    filteredSet3 = processORVariations(filteredSet2, antiVariationOR)

    # Delete empty from the set.
    emptySet = {()}
    refinedSet = filteredSet3 - emptySet

    # Sort the data.
    sortedList = sorted(refinedSet)
    return sortedList


def processNANDVariations(variationSet, antiVariationNAND):
    filteredSet1 = variationSet.copy()

    # Delete impossible variations from the set based on NAND modifier rules.
    for imp in antiVariationNAND:
        for item in variationSet:
            if match(item, imp):
                filteredSet1.discard(item)

    return filteredSet1


def processXNORVariations(filteredSet1, antiVariationXNOR):
    filteredSet2 = filteredSet1.copy()

    # Digging through the nested array.
    for imp in antiVariationXNOR[0]:
        for ymp in imp:
            for omp in ymp:

                # If there's a match with the item to delete, and the List item...
                for item in filteredSet1:
                    if match(item, omp):
                        discardItem = 1

                        # ...compare the List item with another list of things to ignore.
                        # If there's a match at any point, don't delete item.
                        for amp in antiVariationXNOR[1]:
                            for emp in amp:
                                for ump in emp:
                                    if match(item, ump):
                                        discardItem = 0
                        if discardItem == 1:
                            filteredSet2.discard(item)

    return filteredSet2


def processORVariations(filteredSet2, antiVariationOR):
    tries = 0
    matches = 0
    filteredSet3 = filteredSet2.copy()

    # Delete impossible variations from the set based on OR rules.
    for item in filteredSet2:
        tries = 0
        matches = 0

        for imp in antiVariationOR:
            for ymp in imp:
                if ymp != []:
                    tries = tries + 1
                    # print('attempting to match the elements of... ' + str(item) + ' and ' + str(ymp))
                    for omp in ymp:
                        for atem in item:
                            if omp == atem:
                                matches = matches + 1
        if matches < tries:
            # print(str(item) + ' was deleted!')
            filteredSet3.discard(item)

    return filteredSet3


def fillProjection(MDA, sortedList, projection, currentName, currentInputList, prereqsString, modStartCol):
    tempString = ''

    # Add all the variations of the current attack in the projection.
    for xx in sortedList:
        for xxy in xx:
            if tempString == '':
                tempString = tempString + MDA[0][modStartCol + xxy]
            else:
                tempString = tempString + ' + ' + MDA[0][modStartCol + xxy]

        projection[0].append(currentName)
        projection[2].append(currentInputList)
        if prereqsString != '':
            projection[1].append(prereqsString + ' + ' + tempString)
        else:
            projection[1].append(tempString)
        tempString = ''

    return projection


def makePrereqsString(currentActionPrereqs, prereqsString):

    # Makes a string out of the content of currentActionPrereqs.
    prereqsSet = set(currentActionPrereqs)
    for ouh in prereqsSet:
        if prereqsString == '':
            prereqsString = ouh
        else:
            prereqsString = prereqsString + ' + ' + ouh

    return prereqsString


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


def match(combination, match):
    return all(elem in combination for elem in match)


def fixModifiers(masterSheet, modifierDataArray):
    print("TO DO")
