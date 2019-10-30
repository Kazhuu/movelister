def createNewNamedRange(sheet, namedRanges):
    """
    A function that creates a new Named Range based on user requirements.
    TO DO: code for cell range conversion to create base address.
    The CellAddress doesn't seem to do much (other than determine sheet?).
    """

    cellAddress = sheet.getCellByPosition(1, 1).getCellAddress()
    namedRanges.addNewByName("Test Name", "C4:D19", cellAddress, 0)


def deleteNamedRanges(namedRanges):
    for item in namedRanges.getElementNames():
        namedRanges.removeByName(item)
