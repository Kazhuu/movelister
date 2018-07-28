from movelister import cursor, delete, group, inputList, loop, messageBox


def refreshMechanicsList(mechanicsSheet, inputSheet, projectionMaster, projectionMechanics):
    """
    A function that updates and replaces the entire contents of Mechanics List.
    The code follows user-set guidelines from Master List, Modifier List and Input
    List to know what the finished Mechanics List should look like. The code works,
    but there's still a bug or two.

    Known bug 1: if user removes something from an Input List, it won't be removed
    from already existing actions in Mechanics List.
    """
    mda = cursor.getSheetContent(mechanicsSheet)
    actionInputCheck = projectionMaster[2].copy()
    currentActionArray = []
    updatedList = mda[0:2]

    # First initialization of currentInputList.
    currentInputList = projectionMaster[2][0]
    inputListContents = inputList.getSpecificInputList(inputSheet, currentInputList)
    print('Input list changed to: ' + str(currentInputList))

    # Start going through Master List Projection.
    for a in range(len(projectionMaster[0])):
        nameMatch = 0
        lengthMatch = 0

        # Check if the most recently loaded Input List matches current animation. If not, then update it.
        if currentInputList != projectionMaster[2][a]:
            currentInputList = projectionMaster[2][a]
            inputListContents = inputList.getSpecificInputList(inputSheet, currentInputList)
            print('Input list changed to: ' + str(currentInputList))

        # Compare Master List Projection directly with Mechanics List Projection.
        for b in range(len(projectionMechanics[0])):

            # If there's a match between action names...
            if projectionMaster[0][a] == projectionMechanics[0][b] and \
               projectionMaster[1][a] == projectionMechanics[1][b]:
                nameMatch = 1

                # Also compare between projected action length. Returns 1 if it's a match.
                lengthMatch = compareActionLengths(projectionMaster, projectionMechanics, a, b)

                # In case lengths don't match, the code goes to more detailed row generation for this action.
                if lengthMatch == 0:
                    print('Projected lengths did not match.')

                    # Copy correct rows and generate missing rows in currentActionArray (?).
                    updatedList = copyActionDataRowByRow(mda, updatedList, inputListContents, projectionMaster,
                                                         projectionMechanics, a, b)
                    break

                # If the current input list is new to the code, the code examines it to see that it matches too.
                # If it does, then actionInputCheck is updated to show that with the string 'OK!'
                if actionInputCheck[a] != 'OK!':
                    actionInputCheck = updateActionInputCheck(mda, inputSheet, projectionMechanics, currentInputList,
                                                              actionInputCheck, b)

                    # If everything's okay, update updatedList with the temporary data.
                    if actionInputCheck[a] == 'OK!':
                        currentActionArray = mda[projectionMechanics[3][b]:projectionMechanics[3][b + 1]]
                        updatedList = updatedList + currentActionArray
                        break

                    # On the contrary, if there is still a mismatch, then the animation is created row-by-row.
                    else:
                        updatedList = copyActionDataRowByRow(mda, updatedList, inputListContents, projectionMaster,
                                                             projectionMechanics, a, b)
                        break

                # If everything's okay, update updatedList with the temporary data.
                elif actionInputCheck[a] == 'OK!':
                    currentActionArray = mda[projectionMechanics[3][b]:projectionMechanics[3][b + 1]]
                    updatedList = updatedList + currentActionArray
                    break

        # If there was no nameMatch, the new data has to be generated.
        # The correct format is a nested tuple...
        if nameMatch == 0:
            updatedList = generateNewActionData(mda, updatedList, inputListContents, projectionMaster, a)

    # Deleting old contents of Mechanics List. This clears groups and formatting
    # as well as gets rid of extra rows at the bottom.
    lowestRow = len(mda)
    delete.deleteRows(mechanicsSheet, 2, lowestRow)

    # Set new array as sheet contents.
    cursor.setSheetContent(mechanicsSheet, updatedList)


def compareActionLengths(projectionMaster, projectionMechanics, a, b):
    """
    Code that compares between projected action lengths.
    """
    masterActionLength = projectionMaster[3][a + 1] - projectionMaster[3][a]
    mechanicsActionLength = projectionMechanics[3][b + 1] - projectionMechanics[3][b]

    if masterActionLength == mechanicsActionLength:
        return 1
    else:
        return 0


def updateActionInputCheck(mda, inputSheet, projectionMechanics, currentInputList,
                           actionInputCheck, b):
    inputListContents = inputList.getSpecificInputList(inputSheet, currentInputList)
    actionArea = mda[projectionMechanics[3][b]: projectionMechanics[3][b + 1]]

    # Code checks the values between the projected location of current animation and next animation.
    # The code counts how many matches there is between input list and the already listed
    # animation in the Mechanics List.
    x = -1
    inputMatch = -1
    for raw in inputListContents:
        x = x + 1
        for war in actionArea:
            if raw[0] == war[2]:
                inputMatch = inputMatch + 1
                # print(str(raw[0]) + ' matched with ' + str(war[2]))
                break

    # If there's a perfect match, the code remembers that this input list is fine.
    # It is not checked on subsequent actions.
    if inputMatch == x:
        print('perfect match')

        h = -1
        for c in actionInputCheck:
            h = h + 1
            if c == currentInputList:
                actionInputCheck[h] = 'OK!'

    return actionInputCheck


def getMechanicsListProjection(mechanicsSheet, projectionMaster):
    """
    This function creates a projection of what Mechanics List holds at the moment.
    """
    mda = cursor.getSheetContent(mechanicsSheet)
    projectionMechanics = [[], [], [], []]

    if len(mda) > 2:
        currentAction = mda[2][0]
        currentMods = mda[2][1]

        # projectionMechanics is appended with 2, which is the starting point of the data.
        projectionMechanics[3].append(2)

        z = -1
        for row in mda:
            z = z + 1

            if row[0] == '' and z > 1:
                projectionMechanics[0].append(currentAction)
                projectionMechanics[1].append(currentMods)
                projectionMechanics[3].append(z + 1)
                currentAction = mda[z + 1][0]
                currentMods = mda[z + 1][1]

        # The last append happens necessarily outside loop.
        if currentAction != '':
            projectionMechanics[0].append(currentAction)
            projectionMechanics[1].append(currentMods)
            projectionMechanics[3].append(z + 1)

        # Fill index [2] with the help of the Master List Projection.
        for actionML in projectionMechanics[0]:
            x = -1
            match = 0
            for action in projectionMaster[0]:
                x = x + 1
                if actionML == action:
                    projectionMechanics[2].append(projectionMaster[2][x])
                    match = 1
                    break
            if match == 0:
                projectionMechanics[2].append('')

    return projectionMechanics


def generateNewActionData(mda, updatedList, inputListContents, projectionMaster, a):

    # Generate an empty List that is as wide as the Mechanics List.
    tempList = []

    for z in range(len(mda[0])):
        tempList.append('')

    emptyTupleRow = convertIntoNestedTuple(tempList)

    for raw in inputListContents:
        if raw[0] != '':
            tempList[0] = projectionMaster[0][a]
            tempList[1] = projectionMaster[1][a]
            tempList[2] = raw[0]

            # Converting back to a nested tuple and updating final list row by row.
            tempTuple = convertIntoNestedTuple(tempList)
            updatedList = updatedList + tempTuple

    # Add one more empty row to mark the start of a new animation.
    updatedList = updatedList + emptyTupleRow

    return updatedList


def convertIntoNestedTuple(list):
    # This code converts an 1d List into a 2d Tuple that is compatible with a data array of a sheet.

    tempTuple2 = tuple(list)
    tempList3 = [[]]
    tempList3[0] = tempTuple2
    tempTuple4 = tuple(tempList3)

    return tempTuple4


def copyActionDataRowByRow(mda, updatedList, inputListContents, projectionMaster, projectionMechanics, a, b):
    tempTuple = mda[1:2]
    tempList = list(tempTuple[0])
    emptyTupleRow = mda[1:2]
    actionArea = mda[projectionMechanics[3][b]: projectionMechanics[3][b + 1]]

    # Code compares input list to what exists in Mechanics List (represented by mda).
    # If there is a match, the whole row is copied to updatedList.
    z = -1
    for raw in inputListContents:
        z = z + 1
        match = 0
        for war in actionArea:
            if raw[0] == war[2]:
                print('There was a match with: ' + str(raw[0]) + ' ' + str(war[2]))
                tempTuple = actionArea[z:z+1]
                updatedList = updatedList + tempTuple
                match = 1
                break

        # If there was no match, then the row is generated instead.
        if match == 0:
            print('Generating ' + str(raw[0]))
            tempList[0] = projectionMaster[0][a]
            tempList[1] = projectionMaster[1][a]
            tempList[2] = raw[0]

            # Converting back to a nested tuple and updating final list row by row.
            tempTuple2 = tuple(tempList)
            tempList3 = [[]]
            tempList3[0] = tempTuple2
            tempTuple4 = tuple(tempList3)
            updatedList = updatedList + tempTuple4

    # Add one more empty row to mark the start of a new animation.
    updatedList = updatedList + emptyTupleRow

    return updatedList


def setColors(mechanicsSheet, actionColors, modifierColors, inputColors):
    print('TO DO')


def generateGroupsFromArray(mechanicsSheet, inputGroups, startRow):
    x = 0
    groupStartRow = -1
    groupEndRow = -1
    currentGroup = -1

    # Loop figures out the points where inputGroups array changes and groups accordingly.
    while x < len(inputGroups):
        if currentGroup != -1:
            if inputGroups[x] != currentGroup or x == len(inputGroups) - 1:
                groupEndRow = x
                if x == len(inputGroups) - 1:
                    groupEndRow = groupEndRow + 1
                group.groupRows(mechanicsSheet, groupStartRow + startRow, groupEndRow + startRow - 1)
                groupStartRow = -1
                currentGroup = -1
        if inputGroups[x] != '':
            if groupStartRow == -1:
                groupStartRow = x
                currentGroup = inputGroups[x]
        x = x + 1

    # Test printing out the inputGroups array.
    y = 0
    while y < len(inputGroups):
        mechanicsSheet.getCellByPosition(7, y + startRow).setString(inputGroups[y])
        y = y + 1


def generatePhases(mechanicsSheet, highestPhase, phaseCount):
    phasesStart = loop.getColumnPosition(mechanicsSheet, '> Phase 0 result') - 1
    amount = (highestPhase - phaseCount) * 3
    startCol = phasesStart + ((phaseCount + 1) * 3)
    str1 = '> Phase '
    str2 = ' result'

    print(startCol)
    print(amount)
    mechanicsSheet.Columns.insertByIndex(startCol, amount)

    # A loop that generates three Columns per phase.
    # It also generates specific details for each Column.
    phasePart = 0
    loopC = 1
    x = 0
    while x < amount:
        if phasePart == 0:
            mechanicsSheet.getColumns().getByIndex(startCol + x).Width = 1850
            # To do: Add Data Validation for Reactions on this column.
        if phasePart == 1:
            # mechanicsSheet.getColumns().getByIndex(startCol + x).OptimalWidth = 1
            mechanicsSheet.getColumns().getByIndex(startCol + x).Width = 4700
            mechanicsSheet.getCellByPosition(startCol + x, 0).setString(str1 + str(phaseCount + loopC) + str2)
            # To do: Add Data Validation for Actions on this column.
        if phasePart == 2:
            mechanicsSheet.getColumns().getByIndex(startCol + x).Width = 2000
            # To do: Add Data Validation for Modifiers on this column.
        phasePart = phasePart + 1
        if phasePart > 2:
            phasePart = 0
            loopC = loopC + 1
        x = x + 1


def deletePhases(mechanicsSheet, highestPhase, phaseCount):
    phasesStart = loop.getColumnPosition(mechanicsSheet, '> Phase 0 result') - 1
    amount = (phaseCount - highestPhase) * 3
    startCol = phasesStart + (((phaseCount + 1) * 3)) - (amount)
    titleText = 'Warning:'
    messageText = 'Phase columns are about to be deleted and data may become lost. Do you want to continue?'

    # A messagebox warning user that some data may become lost.
    result = messageBox.createMessage('YES_NO', titleText, messageText)

    if result == 'YES':
        delete.deleteColumns(mechanicsSheet, startCol, amount)


def countPhases(mechanicsSheet):
    # Mechanics Sheet top row is iterated through twice to figure out how many columns are taken by Phases.
    phasesStart = loop.getColumnPosition(mechanicsSheet, '> Phase 0 result')
    phasesEnd = loop.getColumnPosition(mechanicsSheet, 'Notes 1')

    # Small math operation to get the actual number of phases.
    phaseNum = (phasesEnd - phasesStart - 2) / 3
    print(phaseNum)
    return phaseNum
