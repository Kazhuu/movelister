from movelister import loop


def getModifierList(modifierSheet):
    x = 1
    endRow = -1

    # The loop iterates through Modifier List to get its end row.
    # The loop breaks once there are two empty rows or x is over 1000.
    endRow = loop.getEndOfList(modifierSheet)

    # The four attributes for CellRangeByPosition are: left, top, right, bottom.
    # To do: the wideness of this array isn't well defined yet. It depends on
    # what's all the data that's actually needed elsewhere.
    range = modifierSheet.getCellRangeByPosition(0, 1, 4, endRow)

    masterDataArray = range.getDataArray()
    return masterDataArray


def getModifierListColors(modifierSheet, listLength):
    x = 1
    modifierColors = []

    # Iterate through Results List second column to get a list of colors.
    while x < listLength + 1:
        modifierColors.append(modifierSheet.getCellByPosition(2, x).CellBackColor)
        x = x + 1

    return modifierColors
