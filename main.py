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

from movelister import conditionalFormat, delete, environment, group, inputList, mechanicsList, test  # nopep8


def generateSingleAction(**kwargs):
    model = environment.getDocument(**kwargs)
    masterSheet = model.Sheets.getByName('Master Action List')
    inputSheet = model.Sheets.getByName('Input Lists')
    mechanicsSheet = model.Sheets.getByName('Mechanics Test')

    # To do: a function that figures out if a new Action has to be generated in Mechanics List.
    # Also: what position it should be in.

    # To do: a function that figures out which Input List the new Action will use.

    # A function that gets all relevant data from Input Lists sheet.

    inputGroupName = 'Default'
    inputDataArray = inputList.getInputList(inputSheet, inputGroupName)
    inputColors = inputList.getInputColors(inputSheet, inputDataArray)

    # A function that generates empty rows in Mechanics List and prints the data.
    # Note: still incomplete! See MechanicsList.py
    startRow = 2
    nameField1 = 'Test'
    nameField2 = 'Modifier'

    mechanicsList.generateAction(mechanicsSheet, inputDataArray, inputColors, nameField1, nameField2, startRow)
    # test.testItOut(inputSheet, inputDataArray)

    # To do: a function probably has to re-generate Conditional Formatting after larger operations.


def deleteSingleAction(**kwargs):
    model = environment.getDocument(**kwargs)
    masterSheet = model.Sheets.getByName('Master Action List')
    inputSheet = model.Sheets.getByName('Input Lists')
    mechanicsSheet = model.Sheets.getByName('Mechanics Test')

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


def generatePhases(**kwargs):
    model = environment.getDocument(**kwargs)
    masterSheet = model.Sheets.getByName('Master Action List')
    mechanicsSheet = model.Sheets.getByName('Mechanics Test')

    # To do: a function that figures out if more phases need to be drawn on Mechanics List.
    # Also: what position they have to be in.

    # To do: a function that generates three rows per Phase and gives them correct length.

    # To do: a function has to generate Data Validation for any new columns that are created.

    # To do: a function has to re-generate Conditional Formatting for the new area.


def deletePhases(**kwargs):
    model = environment.getDocument(**kwargs)
    masterSheet = model.Sheets.getByName('Master Action List')
    mechanicsSheet = model.Sheets.getByName('Mechanics Test')

    # To do: a function that figures out if there are redundant phases drawn on Mechanics List.

    delete.deleteColumns(mechanicsSheet, 2, 2)


def createConditionalFormatting(**kwargs):
    model = environment.getDocument(**kwargs)
    sheet = model.Sheets.getByName('Mechanics Test')
    resultsSheet = model.Sheets.getByName('Results List')

    # A function that gets all relevant data from the Results Sheet.
    resultsList = conditionalFormat.getResultsList(resultsSheet)
    resultsListColors = conditionalFormat.getResultsListColors(resultsSheet, len(resultsList))

    # A function that uses the gathered data and generates the formatting.
    # Note: still incomplete! See conditionalFormat.py
    conditionalFormat.applyConditionalFormatting(sheet, resultsList, resultsListColors)


# Run when executed from the command line.
if __name__ == '__main__':
    generateSingleAction(host='localhost', port=2002)
