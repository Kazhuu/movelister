from movelister import convert, cursor, formatting, loop, modifierList

SPACE_VIEW = ' ' * 11
SPACE_INPUT = ' ' * 5
SPACE_NAME = ' ' * 15
SPACE_NOTES = ' ' * 52


def generateMasterList(document, modifierSheet, aboutSheet, sheetName):
    """
    This function generates an entire Master List sheet from nothing.
    """
    document.Sheets.insertNewByName(sheetName, 1)
    newMasterSheet = document.Sheets.getByIndex(1)

    # Create the text for the title bar and makes it into a nested tuple.
    # The first version of the text has a lot of unnecessary space in it to make column width the right size.
    modifiers = modifierList.getModifierListProjection(modifierSheet)
    titleBarStart = ['Action Name' + SPACE_NAME, 'Color', 'Hit', 'Frames', 'Phase', 'DEF']
    titleBarEnd = ['Notes 1' + SPACE_NOTES, 'Notes 2' + SPACE_NOTES, 'Notes 3' + SPACE_NOTES]
    titleBarFinal = titleBarStart + modifiers + titleBarEnd
    titleBarTuple = convert.convertIntoNestedTuple(titleBarFinal)

    # Sets text with space into the sheet and sets column lengths right.
    cursor.setSheetContent(newMasterSheet, titleBarTuple)
    formatting.setOptimalWidthToRange(newMasterSheet, 0, len(titleBarTuple[0]))

    # Update text with space with regular text that doesn't have space.
    titleBarStart = ['Action Name', 'Color', 'Hit', 'Frames', 'Phase', 'DEF']
    titleBarEnd = ['Notes 1', 'Notes 2', 'Notes 3']
    titleBarFinal = titleBarStart + modifiers + titleBarEnd
    titleBarTuple = convert.convertIntoNestedTuple(titleBarFinal)

    # To do: set data from Overview into the sheet as well.
    # To do: leave 1 empty row at the top to leave room for HUD.

    startCol = loop.getColumnPosition(newMasterSheet, 'DEF') + 1
    endCol = loop.getColumnPosition(newMasterSheet, 'Notes 1')
    modifierColors = loop.getColorArray(modifierSheet)

    # Set formatting.
    formatting.setHorizontalAlignmentToSheet(newMasterSheet, 'CENTER')
    formatting.setTitleBarColor(newMasterSheet, aboutSheet, 0)
    formatting.setMasterListModifierColors(newMasterSheet, startCol, endCol, modifierColors)

    # TO DO: set Bold text. Needs some textCursor object?

    # To do: Set freeze? (model).freezeAtPosition(nCol, nRow)

    # To DO: create a button for user interface?


def generateMechanicsList(document, aboutSheet, sheetName):
    """
    This function generates an entire Mechanics / Details List from nothing.
    """
    document.Sheets.insertNewByName(sheetName, 1)
    newDetailsSheet = document.Sheets.getByIndex(1)

    # TO DO: the rest.


def generateEmptyTupleRow(length):
    """
    The purpose of this code is to create an empty row that is as wide as the current
    sheet and also compatible with the cursor module.
    """
    emptyList = []
    x = length

    for i in range(x):
        emptyList.append([])

    emptyTupleRow = convert.convertIntoNestedTuple(emptyList)

    print(emptyTupleRow)
    return emptyTupleRow
