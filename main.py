"""
Main file for the all usable LibreOffice macros. Can also be executed from the
command line and connect to opened LibreOffice socket.
"""
import uno  # noqa
import os
import sys

# This is to emulate how LibreOffice adds pythonpath folder to PYTHONPATH where
# the script is executed. PYTHONPATH is added when executing from the command
# line.
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname('__file__'), 'pythonpath'))

from movelister.context import Context  # noqa
from movelister.sheet import Sheet  # noqa
from movelister import color, conditionalFormat, cursor, delete, dev, error, generate, group, inputList, loop, \
    masterList, mechanicsList, messageBox, modifierList, namedRanges, resultsList, test, validation  # noqa

# Setup context automatically when macro is run from the LibreOffice.
if __name__ != '__main__':
    Context.setup()


def setColor():
    """
    Test macro to test Color class and setting color.
    """
    modifierSheet = Sheet.getModifierList()
    c = color.Color(modifierSheet.getCellByPosition(0, 0).CellBackColor)
    c.alpha = 0
    c.red = 0
    c.green = 0
    c.blue = 255
    print(hex(c.value))
    modifierSheet.getCellByPosition(0, 0).CellBackColor = c.value


def copySheet():
    """
    Test macro to copy entire sheet to another one using cursor.
    """
    sheet = Sheet.getMasterActionList()
    newSheet = Sheet.newSheet('copy', 1)
    data = cursor.getSheetContent(sheet)
    cursor.setSheetContent(newSheet, data)


def generateOrRefreshMechanicsList():
    """
    A very general function that creates / refreshes full mechanics list up to date with a single button.
    If the project has multiple views / Mechanics Lists, there would probably be some drop down menu
    pointing the code to the correct List before the code is ran.
    """
    masterSheet = Sheet.getMasterActionList()
    inputSheet = Sheet.getInputList()
    mechanicsSheet = Sheet.getMechanicsList()
    modifierSheet = Sheet.getModifierList()

    # TO DO: name is a placeholder value. Eventually, once UI is implemented, user can choose it.
    name = 'Default'
    sheetName = 'Mechanics List (' + name + ')'

    # A bit of error checking at the start.
    result = error.listGenerationNameCheck(document, sheetName)

    if result == 'GENERATE':
        print()
        # TO DO: a function that generates the template of Mechanics List from nothing.
        # The code then segues into the usual "refresh" code that updates the info inside the List.
    elif result == 'NO':
        exit()

    # The code goes through Master Action List and makes a "projection" of what the Mechanics List should
    # look like. It's a multi-dimensional array where [0] lists action name, [1] lists modifiers, [2] lists
    # input list and [3] lists the expected location of the action in Mechanics List.
    projectionMaster = masterList.getMasterListProjection(masterSheet, modifierSheet, inputSheet)

    # Same thing for what is currently inside Mechanics List.
    projectionMechanics = mechanicsList.getMechanicsListProjection(mechanicsSheet, projectionMaster)

    # Code creates a new Array which is eventually pasted on mechanicsList, replacing it
    # entirely in a single swoop. (It's faster to do it like this than generate row-by-row.)
    mechanicsList.refreshMechanicsList(mechanicsSheet, inputSheet, projectionMaster, projectionMechanics)

    # TO DO: regenerate conditional formatting.
    # TO DO: color cell backgrounds according to info. There are basically three types of coloring:
    # action colors, modifier colors and input colors.
    actionColors = loop.getColorArray(masterSheet)
    modifierColors = loop.getColorArray(modifierSheet)
    inputColors = loop.getColorArray(inputSheet)

    mechanicsList.setColors(mechanicsSheet, actionColors, modifierColors, inputColors)

    # TO DO: group rows according to info in Input List.


def generateOrRefreshMasterList():
    document = Context.getDocument()
    aboutSheet = Sheet.getAbout()
    modifierSheet = Sheet.getModifierList()

    # TO DO: name is a placeholder value. Eventually, once UI is implemented, user can choose it.
    name = 'Default'
    sheetName = 'Master List (' + name + ')'

    # A bit of error checking at the start.
    result = error.listGenerationNameCheck(document, sheetName)

    if result == 'GENERATE':
        generate.generateMasterList(document, modifierSheet, aboutSheet, sheetName)
    elif result == 'YES':
        print()
        # To do: go to Master List refresh function.
    else:
        exit()

    # How to define the position of the new document? Group it with other Master Action Lists?
    # Leave it up to the user to move it?


def namedRangeTest():
    """
    Quick tests with named ranges.
    """
    mechanicsSheet = Sheet.getMechanicsList()
    namedRange = Context.getDocument().NamedRanges
    namedRanges.deleteNamedRanges(namedRange)
    namedRanges.createNewNamedRange(mechanicsSheet, namedRange)


def refreshPhases():
    """
    A test function for removing or adding phases in Mechanics List. Seems to work,
    but the code could probably be more elegant.
    """
    masterSheet = Sheet.getMasterActionList()
    mechanicsSheet = Sheet.getMechanicsList()

    # A function that fetches Master Action List to fetch its highest phase number.
    # To do: to be more flexible, the code should also take into account if the high phase numbers
    # are actually USED at all in the Mechanics List.
    masterDataArray = masterList.getMasterList(masterSheet)
    highestPhase = masterList.getHighestPhaseNumber(masterSheet, len(masterDataArray))

    # A function that counts the phases in the Mechanics List.
    phaseCount = mechanicsList.countPhases(mechanicsSheet)

    # Comparing the highest known Phase number in Master Action List vs Mechanics List phase number
    # and determining if new phases have to be added or deleted.
    if highestPhase == phaseCount:
        print('No need to add or delete phases.')
    if highestPhase > phaseCount:
        mechanicsList.generatePhases(mechanicsSheet, highestPhase, phaseCount)
    if highestPhase < phaseCount:
        mechanicsList.deletePhases(mechanicsSheet, highestPhase, phaseCount)

    # To do: a function may have to re-generate Conditional Formatting for the sheet.


def refreshModifiers():
    """
    A function that refreshes the modifier block of Master List based on the data
    the user has set inside Modifier List. This includes the number and position of
    various modifiers as well as their color.
    """
    masterSheet = Sheet.getMasterActionList()
    modifierSheet = Sheet.getModifierList()

    # A function that creates a Data Array of the whole Modifier List.
    # A separate array is created for the cell background color data.
    modifierListModifiers = modifierList.getModifierListProjection(modifierSheet)
    modifierColors = loop.getColorArray(modifierSheet)

    # Function compares this data to the Modifiers columns in Master Action List.
    # It then deletes unnecessary Modifier columns or add necessary Modifier Columns in Master Action List.
    # It then colors the cell background of the columns.
    masterList.updateMasterListModifiers(masterSheet, modifierListModifiers, modifierColors)


def createConditionalFormatting():
    """
    A test function for just setting up quick conditional formatting.
    """
    mechanicsSheet = Sheet.getMechanicsList()
    resultsSheet = Sheet.getResultsList()

    # A function that gets all relevant data from the Results Sheet.
    resultsDataArray = resultsList.getResultsList(resultsSheet)
    resultsColors = loop.getColorArray(resultsSheet)

    # A function that uses the gathered data and generates the formatting.
    # Note: still incomplete! See conditionalFormat.py
    conditionalFormat.applyConditionalFormatting(mechanicsSheet, resultsDataArray, resultsColors)
    # conditionalFormat.clearConditionalFormatting(mechanicsSheet)


# Run when executed from the command line.
if __name__ == '__main__':
    Context.setup(host='localhost', port=2002)
    generateOrRefreshMasterList()
