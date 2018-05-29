def getMasterList(masterSheet):
    x = 1
    endRow = -1

    # The loop iterates through Master Action List to get its coordinates.
    # The loop breaks once there are two empty rows or x is over 1000.
    while x < 1000:
        if masterSheet.getCellByPosition(0, x).getString() == '':
            if masterSheet.getCellByPosition(0, x + 1).getString() == '':
                        endRow = x - 1
                        break
        x = x + 1

    # The four attributes for CellRangeByPosition are: left, top, right, bottom.
    # Figure out if there is some better way to define the wideness of this array.
    # What is all the information that's actually needed? Should it also include Modifiers?
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
    while x <= listLength:
        x = x + 1
        if masterSheet.getCellByPosition(3, x).getValue() == phase:
            phase = phase + 1
            x = -1

    phase = phase - 1
    return(phase)
