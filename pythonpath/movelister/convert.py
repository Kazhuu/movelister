def convertIntoNestedTuple(list):
    # This code converts an 1d List into a 2d Tuple that is compatible with a data array of a sheet.

    tempTuple2 = tuple(list)
    tempList3 = [[]]
    tempList3[0] = tempTuple2
    tempTuple4 = tuple(tempList3)

    return tempTuple4
