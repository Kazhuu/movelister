"""
Main file for the all usable LibreOffice macros. Can also be executed from the
command line and connect to opened LibreOffice socket.
"""
import os
import sys

# This is to emulate how LibreOffice adds pythonpath folder to PYTHONPATH where
# the script is executed. PYTHONPATH is added when executing from the command
# line.
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname('__file__'), 'pythonpath'))

from movelister.context import Context  # noqa
from movelister.sheet import Sheet  # noqa
from movelister import conditionalFormat, delete, group, inputList, masterList, \
    mechanicsList, messageBox, modifierList, resultsList, test, dev, color, cursor  # noqa

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


def generateMechanicsList():
    masterSheet = Sheet.getMasterActionList()
    inputSheet = Sheet.getInputList()
    mechanicsSheet = Sheet.getMechanicsList()
    modifierSheet = Sheet.getModifierList()

    # A very general function that creates / refreshes full mechanics list up to date with a single button.
    # If the project has multiple views / Mechanics Lists, there would probably be some drop down menu
    # pointing the code to the correct List before the code is ran.

    # TO DO: a function that determines if there is a Mechanics List in the file. If not,
    # it has to be generated from scratch? Or for now, the code gives the user a message
    # saying they need to have the template open.

    # The code goes through Master Action List and makes a "projection" of what the Mechanics List should
    # look like. It's a multi-dimensional array where one part lists how many rows a single animation takes.
    # (Based on data in Input List). (?) Other part list the action name and modifier name.
    masterList.getMasterListProjection(masterSheet, modifierSheet)

    # TO DO: a function for a quick comparison of the contents of Master Action List and Mechanics List.
    # TO DO: the code creates a new Array which is eventually pasted on mechanicsList, replacing it
    # entirely in a single swoop. (It's faster to do it like this than generate row-by-row.) The wideness
    # of the array is determined by the amount of columns in the Mechanics List because it will also include
    # user-generated data.

    # The code starts going through Mechanics List using the projection and data from Input Lists.
    # It first checks if the animation in Mechanics List exists in MAL. If not, it's skipped entirely.
    # It checks if the animation is already listed...?
    # It checks if the animation is in wrong order. If yes, the data is fetched from a different place. It would help
    # if there was some very simple array of the contents of Mechanics List for faster iteration / comparison?
    # OR if misplaced data is used, perhaps the code would leave a mark somewhere - on an unused column? -
    # or inside the array? To indicate the code that this animation is already dealt with.

    # If there is a match, the code goes through the Action row by row to see if all the Inputs are correct.
    # If the input is correct, the code copies the entire ROW (including user-created data) based on the correct
    # input inside a new Array. If an input is incorrect, the code iterates through the Input List to see if
    # it's a case of a redundant input (it's skipped), a misplaced input (it's copied in the new Array in
    # a new, correct location) or a missing input (it's created based in the new Array).

    # Once a single animation is complete, the code leaves one empty row in the new Array. In addition, it
    # should probably leave some kind of a mark somewhere to indicate that this action is now copied / done.

    # The code goes through the whole list like this. Then...

    # TO DO: the code deletes all the rows below row 0 in Mechanics List. (This way you don't have to
    # delete groups / erase background colors, etc. separately and clean up the List for pasting new array.)

    # TO DO: paste new array and hope all the data is there.
    # TO DO: regenerate conditional formatting.
    # TO DO: regenerate cell background colors.
    # TO DO: group rows according to info in Input List.


def generateSingleAction():
    masterSheet = Sheet.getMasterActionList()
    inputSheet = Sheet.getInputList()
    mechanicsSheet = Sheet.getMechanicsList()

    # To do: a function that figures out if a new Action has to be generated in Mechanics List.
    # Also: what position it should be in.

    # To do: a function that figures out which Input List the new Action will use.

    # A function that gets all relevant data from Input Lists sheet.

    inputGroupName = 'Default'
    inputDataArray = inputList.getInputList(inputSheet, inputGroupName)
    inputColors = inputList.getInputColors(inputSheet, len(inputDataArray))

    # A function that generates empty rows in Mechanics List and prints the data.
    # Note: the data printing part is still incomplete! See MechanicsList.py
    startRow = 2
    nameField1 = 'Test'
    nameField2 = 'Modifier'
    mechanicsList.generateAction(mechanicsSheet, inputDataArray, inputColors, nameField1, nameField2, startRow)

    # To do: a function probably has to re-generate Conditional Formatting after larger operations.

    # To do: the code should generate a Named Range for the animation if we start using those.


def deleteSingleAction():
    masterSheet = Sheet.getMasterActionList()
    inputSheet = Sheet.getInputList()
    mechanicsSheet = Sheet.getMechanicsList()

    # To do: a function that figures out if an old Action has to be deleted from Mechanics List.
    # Also: what position it's in.

    # To do: a function that figures out which Input List the old Action used.

    # Placeholder values.
    inputGroupName = 'Default'
    inputDataArray = inputList.getInputList(inputSheet, inputGroupName)
    startRow = 2

    delete.deleteRows(mechanicsSheet, startRow, len(inputDataArray) + 1)

    # To do: a function that deletes Action's Named Range, if we ever start using those.

    # To do: a function probably has to re-generate Conditional Formatting after larger operations.


def refreshPhases():
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
    modifierSheet = Sheet.getModifierList()

    # A function that creates a Data Array of the whole Modifier List.
    # A separate array is created for the cell background color data.
    modifierDataArray = modifierList.getModifierList(modifierSheet)
    modifierListColors = modifierList.getModifierListColors(modifierSheet, len(modifierDataArray))

    print(modifierDataArray)
    print(modifierListColors)

    # To do: compare this data to the Modifiers columns in Master Action List.

    # To do: delete unnecessary Modifier columns or add necessary Modifier Columns
    # in Master Action List.

    # To do: color the cell background of the columns if something was created.


def createConditionalFormatting():
    mechanicsSheet = Sheet.getMasterActionList()
    resultsSheet = Sheet.getResultsList()

    # A function that gets all relevant data from the Results Sheet.
    resultsDataArray = resultsList.getResultsList(resultsSheet)
    resultsListColors = resultsList.getResultsListColors(resultsSheet, len(resultsDataArray))

    # A function that uses the gathered data and generates the formatting.
    # Note: still incomplete! See conditionalFormat.py
    conditionalFormat.applyConditionalFormatting(mechanicsSheet, resultsDataArray, resultsListColors)


# Run when executed from the command line.
if __name__ == '__main__':
    Context.setup(host='localhost', port=2002)
    generateMechanicsList()
