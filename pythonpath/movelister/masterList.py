from movelister import loop


def getMasterList(masterSheet):
    x = 1
    endRow = -1

    # The loop iterates through Master Action List to get its end row.
    # The loop breaks once there are two empty rows or x is over 1000.
    endRow = loop.getEndOfList(masterSheet)

    # The four attributes for CellRangeByPosition are: left, top, right, bottom.
    # To do: the wideness of this array isn't well defined yet. It depends on
    # what's all the data that's actually needed elsewhere.
    range = masterSheet.getCellRangeByPosition(0, 1, 4, endRow)

    masterDataArray = range.getDataArray()
    return masterDataArray


def getHighestPhaseNumber(masterSheet, listLength):
    x = -1
    phase = 0
    check = -1

    # The loop iterates through the Phase column and finds the highest number in sequence.
    # Warning: loop cannot find high phase numbers that are out of sequence.
    # But something like that shouldn't happen in normal use, right?
    # Warning: the loop also doesn't check if the high phase numbers are actually in use,
    # (as indicated by the Modifiers columns) so it doesn't do everything it's supposed to yet.
    while x <= listLength:
        x = x + 1
        if masterSheet.getCellByPosition(3, x).getValue() == phase:
            phase = phase + 1
            x = -1

    phase = phase - 1
    return(phase)
