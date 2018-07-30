from movelister import convert, cursor, formatting, modifierList


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
    titleBarEnd = ['Notes 1                                                    ',
                   'Notes 2                                                    ',
                   'Notes 3                                                    ']
    titleBarFinal = titleBarStart + modifiers + titleBarEnd
    titleBarTuple = convert.convertIntoNestedTuple(titleBarFinal)

    # Sets text with space into the sheet.
    cursor.setSheetContent(newMasterSheet, titleBarTuple)

    # To do: update text with space with regular text that doesn't have space?
    # To do: set data from Overview into the sheet as well.

    # Set formatting.
    formatting.setOptimalWidthToRange(newMasterSheet, 0, len(titleBarTuple[0]))
    formatting.setTitleBarColor(newMasterSheet, aboutSheet, 0)
    formatting.setHorizontalAlignmentToSheet(newMasterSheet, 'CENTER')

    # TO DO: set Bold text. Set background colors.

    # To DO: create a button for user interface?
