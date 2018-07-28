from movelister import convert, cursor, formatting, modifierList


def generateMasterList(document, modifierSheet, name):
    """
    This function generates an entire Master List sheet from nothing.
    """
    sheetName = 'Master List (' + name + ')'
    document.Sheets.insertNewByName(sheetName, 2)
    newMasterSheet = document.Sheets.getByIndex(2)

    # Create the text for the title bar and makes it into a nested tuple.
    modifiers = modifierList.getModifierListProjection(modifierSheet)
    titleBarStart = ['View          ', 'Input List   ', 'Action Name               ', 'Color', 'Hit', 'Frames',
                     'Phase', 'DEF']
    titleBarEnd = ['Notes 1                    ', 'Notes 2                   ', 'Notes 3                     ']
    titleBarFinal = titleBarStart + modifiers + titleBarEnd
    titleBarTuple = convert.convertIntoNestedTuple(titleBarFinal)

    # Sets text into the sheet.
    cursor.setSheetContent(newMasterSheet, titleBarTuple)

    # Set formatting.
    formatting.setOptimalWidthToRange(newMasterSheet, 0, len(titleBarTuple[0]))

    # TO DO: set Bold text. Set background colors.
