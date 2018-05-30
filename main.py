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

from movelister.context import Context  # nopep8
from movelister.sheet import Sheet  # nopep8
from movelister import conditionalFormat, delete, group, inputList, masterList, \
    mechanicsList, messageBox, modifierList, sheet, test  # nopep8

# Setup context automatically when macro is run from the LibreOffice.
if __name__ != '__main__':
    Context.setup()


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
    highestPhase = masterList.getHighestPhaseNumber(masterSheet, len(masterDataArray)) + 1

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
    modifierColors = modifierList.getModifierListColors(modifierSheet, len(modifierDataArray))

    print(modifierDataArray)
    print(modifierColors)

    # To do: compare this data to the Modifiers columns in Master Action List.

    # To do: delete unnecessary Modifier columns or add necessary Modifier Columns
    # in Master Action List.

    # To do: color the cell background of the columns if something was created.


def createConditionalFormatting():
    mechanicsSheet = Sheet.getMasterActionList()
    resultsSheet = Sheet.getResultsList()

    # A function that gets all relevant data from the Results Sheet.
    resultsList = conditionalFormat.getResultsList(resultsSheet)
    resultsListColors = conditionalFormat.getResultsListColors(resultsSheet, len(resultsList))

    # A function that uses the gathered data and generates the formatting.
    # Note: still incomplete! See conditionalFormat.py
    conditionalFormat.applyConditionalFormatting(mechanicsSheet, resultsList, resultsListColors)


# Run when executed from the command line.
if __name__ == '__main__':
    Context.setup(host='localhost', port=2002)
    generateSingleAction()
