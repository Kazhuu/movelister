def getInputList(inputSheet, inputGroupName):
    x = 1
    inputsArray = [[0], [0], [0]]

    # The inputs of the desired Input List are iterated into an array.
    # The loop breaks once there are two blank rows in the list.
    while True:
        if inputSheet.getCellByPosition(0, x).getString() == inputGroupName:
            inputsArray[0].append(inputSheet.getCellByPosition(1, x).getString())
            inputsArray[1].append(inputSheet.getCellByPosition(3, x).CellBackColor)
            inputsArray[2].append(inputSheet.getCellByPosition(4, x).getString())
        if inputSheet.getCellByPosition(0, x).getString() == "":
            if inputSheet.getCellByPosition(0, x + 1).getString() == "":
                break
        x = x + 1
    return inputsArray
