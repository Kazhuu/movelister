from movelister import convert, cursor, formatting, loop, modifierList


def generateMasterList(document, modifierSheet, aboutSheet, sheetName):
    """
    This function generates an entire Master List sheet from nothing.
    """

    document.Sheets.insertNewByName(sheetName, 1)
    newMasterSheet = document.Sheets.getByIndex(1)

    # Create the text for the title bar and makes it into a nested tuple.
    # The first version of the text has a lot of unnecessary space in it to make column width the right size.
    modifiers = modifierList.getModifierListProjection(modifierSheet)
    titleBarStart = ['View           ', 'Input List    ', 'Action Name               ', 'Color', 'Hit', 'Frames',
                     'Phase', 'DEF']
    titleBarEnd = ['Full Name', 'In-Game Description',
                   'Notes 1                                                    ',
                   'Notes 2                                                    ',
                   'Notes 3                                                    ']
    titleBarFinal = titleBarStart + modifiers + titleBarEnd
    titleBarTuple = convert.convertIntoNestedTuple(titleBarFinal)

    # Sets text with space into the sheet and sets column lengths right.
    cursor.setSheetContent(newMasterSheet, titleBarTuple)
    formatting.setOptimalWidthToRange(newMasterSheet, 0, len(titleBarTuple[0]))

    # To do: update text with space with regular text that doesn't have space.
    # To do: set data from Overview into the sheet as well.

    startCol = loop.getColumnPosition(newMasterSheet, 'DEF') + 1
    endCol = loop.getColumnPosition(newMasterSheet, 'Full Name')
    modifierColors = loop.getColorArray(modifierSheet)

    # Set formatting.
    formatting.setHorizontalAlignmentToSheet(newMasterSheet, 'CENTER')
    formatting.setTitleBarColor(newMasterSheet, aboutSheet, 0)
    formatting.setMasterListModifierColors(newMasterSheet, startCol, endCol, modifierColors)

    # TO DO: set Bold text. Needs some textCursor object?

    # To do: Set freeze? (model).freezeAtPosition(nCol, nRow)

    # To DO: create a button for user interface?


def generateMechanicsList(document):
    print()
    # To do...
