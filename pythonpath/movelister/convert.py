def convertIntoNestedTuple(list):
    """
    This code converts an 1d List into a 2d Tuple that is compatible with a data array of a sheet.
    """
    tempTuple2 = tuple(list)
    tempList3 = [[]]
    tempList3[0] = tempTuple2
    tempTuple4 = tuple(tempList3)

    return tempTuple4


def turnArraySideways(array):
    """
    This code turns a 2d-array so that its columns become rows and vice-versa.
    """
    newList = []

    for item in array[0]:
        newList.append([])

    x = -1
    for row in array:
        x = x + 1
        y = - 1
        for item in row:
            y = y + 1
            newList[y].append(item)

    return newList
