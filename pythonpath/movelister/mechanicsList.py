from movelister import cursor, delete, group, loop, messageBox


def refreshMechanicsList(mechanicsSheet, inputSheet, projectionMaster):
    MDA = cursor.getSheetContent(mechanicsSheet)
    updatedList = cursor.getSheetContent(mechanicsSheet)

    # Creating a projection of what Mechanics List holds at the moment.
    projectionMechanics = createMechanicsListProjection(MDA, projectionMaster)

    # Start going through MDA.


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


def compareProjectionToMechanicsList(mechanicsSheet, projectionMaster):
    print()


def generateAction(mechanicsSheet, inputDataArray, inputColors, nameField1, nameField2, startRow):

    # Generate empty rows according to Input List length.
    mechanicsSheet.Rows.insertByIndex(startRow, len(inputDataArray) + 1)

    # Zip the multi-dimensional inputDataArray into three smaller arrays.
    # However: this seems to make the new array incompatible with setDataArray...
    # Find a solution!
    inputList, notUseful, inputGroups = zip(*inputDataArray)
    # print(inputList)

    # Fill columns for name and modifier. Temporary solution!!
    nameCell1 = mechanicsSheet.getCellByPosition(0, startRow)
    nameCell1.setString(nameField1)
    nameCell2 = mechanicsSheet.getCellByPosition(1, startRow)
    nameCell2.setString(nameField2)

    range = mechanicsSheet.getCellRangeByPosition(0, startRow, 1, len(inputList) - 1 + startRow)
    range.fillAuto(0, 1)
    range = mechanicsSheet.getCellRangeByPosition(1, startRow, 1, len(inputList) - 1 + startRow)
    range.fillAuto(0, 1)

    # Fill column for Input List. Temporary solution!!
    y = 0
    while y < len(inputList):
        mechanicsSheet.getCellByPosition(2, y + startRow).setString(inputList[y])
        y = y + 1

    # Test printing out the inputColors array.
    y = 0
    while y < len(inputGroups):
        mechanicsSheet.getCellByPosition(8, y + startRow).setString(inputColors[y])
        y = y + 1

    # Add Groups automatically based on data in the inputGroups array.
    generateGroupsFromArray(mechanicsSheet, inputGroups, startRow)

    # To do: a function that adds where an Action starts and ends with markings.


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
