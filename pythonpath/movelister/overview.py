import itertools

from movelister import convert, delete, error, formatting, \
    inputList, loop, modifierList, test
from movelister.core import cursor


def getOverview(overviewSheet):
    masterDataArray = cursor.getSheetContent(overviewSheet)
    return masterDataArray


def getOverviewProjection(overviewSheet, modifierSheet, inputSheet):
    mda = getOverview(overviewSheet)
    nameCol = loop.getColumnPosition(overviewSheet, 'Action Name')
    modStartCol = loop.getColumnPosition(overviewSheet, 'DEF')
    modEndCol = loop.getColumnPosition(overviewSheet, 'Full Name') - 1
    modAmount = modEndCol - modStartCol
    currentName = mda[1][nameCol]
    currentInputList = mda[1][nameCol - 1]
    currentActionRow = -1
    projection = [[], [], [], []]
    currentActionDEF = -1
    currentActionMods = [[], []]
    currentActionMods.clear()
    currentActionPrereqs = []
    prereqsString = ''

    # A bit of error checking before starting.
    error.overviewProjectionErrorCheck(mda, nameCol)

    # Get an array of impossible variations (derived from Modifier rules) to compare with the action list later on.
    antiVariationOR = modifierList.getImpossibleVariations(modifierSheet, 'OR')
    antiVariationNAND = modifierList.getImpossibleVariations(modifierSheet, 'NAND')
    antiVariationXNOR = modifierList.getImpossibleVariations(modifierSheet, 'XNOR')
    print('List of OR-rules: ' + str(antiVariationOR))
    print('All impossible variations based on NAND-rules: ' + str(antiVariationNAND))
    print('All impossible variations based on XNOR-rules: ' + str(antiVariationXNOR[0]))
    print('Protected variations (XNOR): ' + str(antiVariationXNOR[1]))

    # Loop through rows of Overview (represented as the multi-dimensional List mda).
    x = 0
    while x < len(mda) - 1:
        x = x + 1
        currentActionRow = currentActionRow + 1

        # currentActionMods has to be appended each row so that it has space for listing all the 'x'
        # per each row of the animation.
        currentActionMods.append([])

        # Loop for going through all modifier columns.
        if currentName == mda[x][nameCol]:
            y = -1
            while y < modAmount:
                y = y + 1

                # If first column (DEF) has 'x', there needs to be a modifier-less default version of the action.
                if mda[x][modStartCol + y] == 'x' and y == 0 and currentActionDEF < 1:
                    currentActionDEF = 1
                    print('There will be a DEF version of ' + currentName)

                # If a column has 'x' in any other circumstance...
                # Collect all the 'x' for each row in a multi-dimensional array currentActionMods.
                if mda[x][modStartCol + y] == 'x' and y > 0:
                    currentActionMods[currentActionRow].append(y)

                # If a cell has 'P' (prerequisite), store it for now.
                if mda[x][modStartCol + y] == 'P' and y > 0:
                    currentActionPrereqs.append(mda[0][modStartCol + y])

        # If currentName doesn't match current row, update it. This signifies the start of a new action.
        if currentName != mda[x][nameCol]:

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
                    projection = fillProjection(mda, sortedList, projection, currentName, currentInputList,
                                                prereqsString, modStartCol)

            # Update currentName with new action and re-initialize variables for next action.
            currentName = mda[x][nameCol]
            currentInputList = mda[x][nameCol - 1]
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
    test.printProjectionTest(projection, overviewSheet)

    return projection


def estimateActionPositionsForProjection(inputSheet, projection):

    # Get lengths of all input lists.
    inputListLengths = inputList.getSpecificInputListLengths(inputSheet)

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


def match(combination, match):
    return all(elem in combination for elem in match)


def fillProjection(mda, sortedList, projection, currentName, currentInputList, prereqsString, modStartCol):
    tempString = ''

    # Add all the variations of the current attack in the projection.
    for xx in sortedList:
        for xxy in xx:
            if tempString == '':
                tempString = tempString + mda[0][modStartCol + xxy]
            else:
                tempString = tempString + ' + ' + mda[0][modStartCol + xxy]

        projection[0].append(currentName)
        projection[2].append(currentInputList)
        if prereqsString != '':
            projection[1].append(prereqsString + ' + ' + tempString)
        else:
            projection[1].append(tempString)
        tempString = ''

    return projection


def makePrereqsString(currentActionPrereqs, prereqsString):
    """
    This function makes a string out of the content of the array currentActionPrereqs.
    """
    prereqsSet = set(currentActionPrereqs)
    for ouh in prereqsSet:
        if prereqsString == '':
            prereqsString = ouh
        else:
            prereqsString = prereqsString + ' + ' + ouh

    return prereqsString


def getOverviewModifiers(overviewSheet):
    """
    This function returns the list of modifiers from a chosen Overview as a list.
    It will probably be replaced by a function from Overview class sooner or later.
    """
    headerRowPosition = loop.getHeaderRowPosition(overviewSheet)
    topRowArray = cursor.getRow(overviewSheet, headerRowPosition)
    startCol = loop.getColumnPosition(overviewSheet, 'DEF') + 1
    endCol = loop.getColumnPosition(overviewSheet, 'Notes 1')
    overviewModifiers = topRowArray[startCol:endCol]

    return overviewModifiers


def updateOverviewModifiers(overviewSheet, overviewModifiers, modifierListModifiers, modifierListColors):
    """
    This function updates the section with Modifiers in the Master List using the data from Modifier List.
    """
    mda = getOverview(overviewSheet)
    startCol = loop.getColumnPosition(overviewSheet, 'DEF') + 1
    endCol = loop.getColumnPosition(overviewSheet, 'Notes 1')
    finalList = []

    # The modifier columns of the existing Overview are copied or generated to a new array, which is then
    # pasted to replace the previous columns.
    newModifierArray = createNewModifierArray(mda, overviewSheet, startCol, modifierListModifiers, overviewModifiers)

    # newModifierArray has to be turned sideways with iteration first.
    finalList = convert.turnArraySideways(newModifierArray)
    print(finalList)

    # Delete existing Modifier Block from Overview, if there is one.
    if endCol - startCol > 1:
        delete.deleteColumns(overviewSheet, startCol, len(overviewModifiers))

    # Create a new number of columns for pasting the newModifierArray array into.
    overviewSheet.Columns.insertByIndex(startCol, len(modifierListModifiers))
    range = overviewSheet.getCellRangeByPosition(startCol, 0, startCol + len(modifierListModifiers) - 1, len(mda) - 1)

    # Set data to sheet.
    range.setDataArray(finalList)

    # Fix column width.
    formatting.setOptimalWidthToRange(overviewSheet, startCol, len(modifierListModifiers))

    # Fix column colors.
    formatting.setOverviewModifierColors(overviewSheet, startCol, endCol, modifierListColors)


def createNewModifierArray(mda, overviewSheet, startCol, modifierListModifiers, overviewModifiers):
    """
    This function creates the new array which is pasted in the Modifier block of Master List sheet.
    """
    newList = []
    tempCol = []

    x = -1
    for col in modifierListModifiers:
        x = x + 1
        match = 0

        y = -1
        for mod in overviewModifiers:
            y = y + 1
            if mod == col:
                tempCol = cursor.getColumn(overviewSheet, startCol + y)
                match = 1
                break

        # If there's no match, code has to generate two extra rows: one for UI, one for header.
        if match == 0:
            tempCol.clear()
            tempCol.append('')
            tempCol.append(col)

            for a in range(len(mda) - 2):
                tempCol.append('')

        # Creating a copy of tempCol to prevent data from being overwritten from
        # newList. Then the copy is appended to newList.
        tempCol2 = tempCol.copy()
        newList.append(tempCol2)

    return newList


def getHighestPhaseNumber(overviewSheet, listLength):
    """
    The loop iterates through the Phase column and finds the highest number in sequence.
    """
    x = -1
    phase = 0
    phaseCol = loop.getColumnPosition(overviewSheet, 'Phase')

    # Warning: loop cannot find high phase numbers that are out of sequence.
    # But something like that shouldn't happen in normal use, right?
    # Warning: the loop also doesn't check if the high phase numbers are actually in use,
    # (as indicated by the Modifiers columns) so it doesn't do everything it's supposed to yet.
    while x <= listLength:
        x = x + 1
        if overviewSheet.getCellByPosition(phaseCol, x).getValue() == phase:
            phase = phase + 1
            x = -1

    return(phase)
