from com.sun.star.table import CellRangeAddress

from movelister import group


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

    # Add markings on certain unused phases to show where an animation starts / ends.
    # Needs a code that reads Master Action List beforehand. To be added!


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
