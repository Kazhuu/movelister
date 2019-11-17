from movelister.format import convert


def createNewNamedRange(sheet, name, namedRanges, startRow, endRow, startCol, endCol):
    """
    A function that creates a new Named Range based on user requirements.
    """
    col1 = convert.convertIntoBaseAddress(startCol)
    col2 = convert.convertIntoBaseAddress(endCol)
    cellAddress = sheet.getCellByPosition(1, 1).getCellAddress()
    string = '$\'' + sheet.Name + '\'.' + '$' + col1 + '$' + str(startRow) + ':' + '$' + col2 + '$' + str(endRow)
    namedRanges.addNewByName(name, string, cellAddress, 0)


def deleteNamedRanges(namedRanges):
    """
    A function that deletes all named ranges in a document. Probably useful to
    invoke whenever code deletes a sheet with named ranges from the document.
    """
    for item in namedRanges.getElementNames():
        namedRanges.removeByName(item)


def deleteFilteredNamedRanges(namedRanges, sheetName):
    """
    A function that deletes all named ranges of a named sheet.
    TODO: still in progress.
    """
    string = '$\'' + sheetName + '\'.'
    for item in namedRanges.getElementNames():
        if item.startswith(string) == True:
            namedRanges.removeByName(item)
