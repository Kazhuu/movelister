def getEndOfList(sheet):
    x = 1
    endRow = -1

    # The loop iterates through a list to figure out where it ends.
    # The loop breaks once there are two empty rows or x is over 1000.
    # Currently only used with Modifier List and Master List.
    # I'm sure there's a better way to programmatically reach the end of a list.
    while x < 1000:
        if sheet.getCellByPosition(0, x).getString() == '':
            if sheet.getCellByPosition(0, x + 1).getString() == '':
                        endRow = x - 1
                        break
        x = x + 1
    return endRow
