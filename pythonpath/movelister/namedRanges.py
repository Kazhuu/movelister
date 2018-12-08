def createNewNamedRange(sheet, namedRanges):
    """
    A function that creates a new Named Range based on user requirements.
    Still in progress. TO DO: code for cell range conversion.
    """
    cellAddress = sheet.getCellByPosition(2, 2).getCellAddress()
    namedRanges.addNewByName("Test Name", "C4:C19", cellAddress, 0)


def deleteNamedRanges(namedRanges):
    for item in namedRanges.getElementNames():
        namedRanges.removeByName(item)
