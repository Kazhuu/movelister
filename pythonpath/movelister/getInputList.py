import uno


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


def testItOut(inputSheet, inputsArray):
    x = 1
    while x < len(inputsArray[0]):
        inputSheet.getCellByPosition(8, x).setString(inputsArray[0][x])
        inputSheet.getCellByPosition(9, x).setString(inputsArray[1][x])
        inputSheet.getCellByPosition(10, x).setString(inputsArray[2][x])
        x = x + 1


def main(*args):
    # Basic things to connect to the document.
    desktop = XSCRIPTCONTEXT.getDesktop()
    model = desktop.getCurrentComponent()
    sheet = model.CurrentController.ActiveSheet
    # Placeholder values.
    inputSheet = model.Sheets.getByName("Input Lists")
    inputGroupName = "Default"

    inputsArray = [[0], [0], [0]]

    inputsArray = getInputList(inputSheet, inputGroupName)
    testItOut(inputSheet, inputsArray)


# Exported services.
g_exportedScripts = (main,)
