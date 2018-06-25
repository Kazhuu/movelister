from movelister import cursor, delete, group, inputList, loop, messageBox


def refreshMechanicsList(mechanicsSheet, inputSheet, projectionMaster):
    MDA = cursor.getSheetContent(mechanicsSheet)
    actionInputCheck = projectionMaster[2]
    currentActionArray = []
    updatedList = MDA[0:2]

    # Known bugs 1: trying to generate too long a list can cause index to go OoB in MDA.
    # Known bugs 2: first action with "Water" input list is not fully generated.

    # Creating a projection of what Mechanics List holds at the moment.
    projectionMechanics = createMechanicsListProjection(MDA, projectionMaster)

    # Start going through Master List Projection.
    for a in range(len(projectionMaster[0])):
        match = 0

        # Compare Master List Projection directly with Mechanics List Projection.
        for b in range(len(projectionMechanics[0])):

            # If there's a match between action names...
            if projectionMaster[0][a] == projectionMechanics[0][b] and \
               projectionMaster[1][a] == projectionMechanics[1][b]:

                match = 1
                print('There is a match: ' + str(projectionMaster[0][a]) + ' ' + str(projectionMaster[1][a]))

                # TO DO: also match between projected action location and length?
                # In case lengths don't match, the code goes to more detailed row generation.

                # The code starts going through MDA row-by-row if current input list is unchecked.
                # If it is, then actionInputCheck is updated to show that yes, the input list is okay.
                if actionInputCheck[a] != 'OK!':
                    actionInputCheck = compareActionWithInputList(MDA, inputSheet, projectionMaster,
                                                                  projectionMechanics, actionInputCheck, a, b)

                else:
                    # Copy correct rows and generate missing rows in currentActionArray (?).
                    print('TO DO: more detailed row handling.')

                # Copy rows of the current attack from MDA into the currentActionArray.
                currentActionArray = MDA[projectionMechanics[3][b]:projectionMechanics[3][b + 1]]

                # Update updatedList with the temporary data.
                updatedList = updatedList + currentActionArray
                break

        # If there was no match, the new data has to be generated.
        # The correct format is a nested tuple...
        if match == 0:
            currentInputList = projectionMaster[2][a]
            inputListContents = inputList.getInputList(inputSheet, currentInputList)
            updatedList = generateNewActionData(MDA, updatedList, inputListContents, projectionMaster, a)

    # Deleting old contents of Mechanics List. This clears groups and formatting
    # as well as gets rid of extra rows at the bottom.
    lowestRow = len(MDA)
    delete.deleteRows(mechanicsSheet, 2, lowestRow)

    # Set new array as sheet contents.
    cursor.setSheetContent(mechanicsSheet, updatedList)


def compareActionWithInputList(MDA, inputSheet, projectionMaster, projectionMechanics, actionInputCheck, a, b):
    currentInputList = projectionMaster[2][a]
    inputListContents = inputList.getInputList(inputSheet, currentInputList)

    # Code checks the values between the projected location of current animation and next animation.
    x = projectionMechanics[3][b] - 1
    inputIndex = -1
    inputMatch = -1
    while x < projectionMechanics[3][b + 1] - 1:
        x = x + 1
        inputIndex = inputIndex + 1

        # The code counts how many matches there is between input list and the already listed
        # animation in the Mechanics List.
        if MDA[x][2] == inputListContents[inputIndex][0]:
            inputMatch = inputMatch + 1

    # If there's a perfect match, the code remembers that this input list is fine.
    # It is not checked on subsequent actions.
    if inputMatch == inputIndex:
        print('perfect match')

        h = -1
        for c in actionInputCheck:
            h = h + 1
            if c == currentInputList:
                actionInputCheck[h] = 'OK!'

    return actionInputCheck


def createMechanicsListProjection(MDA, projectionMaster):
    currentAction = MDA[2][0]
    currentMods = MDA[2][1]
    projectionMechanics = [[], [], [], []]

    # Creating a projection of what Mechanics List holds at the moment.
    z = -1
    projectionMechanics[3].append(2)

    for row in MDA:
        z = z + 1

        if row[0] == '' and z > 1:
            projectionMechanics[0].append(currentAction)
            projectionMechanics[1].append(currentMods)
            projectionMechanics[3].append(z + 1)
            currentAction = MDA[z + 1][0]
            currentMods = MDA[z + 1][1]

    # The last append happens necessarily outside loop.
    projectionMechanics[0].append(currentAction)
    projectionMechanics[1].append(currentMods)
    projectionMechanics[3].append(z)

    # Fill index [2] with the help of the Master List Projection.
    x = -1
    for actionML in projectionMechanics[0]:
        x = 0
        for action in projectionMaster[0]:
            x = x + 1
            if actionML == action:
                projectionMechanics[2].append(projectionMaster[2][x])
                break
            else:
                projectionMechanics[2].append('')

    return projectionMechanics


def generateNewActionData(MDA, updatedList, inputListContents, projectionMaster, a):
    tempTuple = MDA[1:2]
    tempList = list(tempTuple[0])
    emptyTupleRow = MDA[1:2]

    for raw in inputListContents:
        if raw[0] != '':
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
    phasesStart = loop.getColumnLocation(mechanicsSheet, '> Phase 0 result') - 1
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
    phasesStart = loop.getColumnLocation(mechanicsSheet, '> Phase 0 result') - 1
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
    phasesStart = loop.getColumnLocation(mechanicsSheet, '> Phase 0 result')
    phasesEnd = loop.getColumnLocation(mechanicsSheet, 'Notes 1')

    # Small math operation to get the actual number of phases.
    phaseNum = (phasesEnd - phasesStart - 2) / 3
    print(phaseNum)
    return phaseNum
