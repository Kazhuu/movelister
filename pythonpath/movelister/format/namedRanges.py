from movelister.format import convert


def createNewNamedRange(sheet, namedRanges):
    """
    A function that creates a new Named Range based on user requirements.
    TO DO: build function using the base address converting function.
    """

    cellAddress = sheet.getCellByPosition(1, 1).getCellAddress()
    namedRanges.addNewByName("Test Name", "C4:D19", cellAddress, 0)


def deleteNamedRanges(namedRanges):
    for item in namedRanges.getElementNames():
        namedRanges.removeByName(item)
