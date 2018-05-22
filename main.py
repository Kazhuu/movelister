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

from movelister import environment, group, inputList, mechanicsList, test, conditionalFormat  # nopep8


def generateSingleAction(**kwargs):
    model = environment.getDocument(**kwargs)

    # Get all relevant data from Input Lists sheet.
    inputSheet = model.Sheets.getByName('Input Lists')
    inputGroupName = 'Default'
    inputDataArray = inputList.getInputList(inputSheet, inputGroupName)
    inputColors = inputList.getInputColors(inputSheet, inputDataArray)

    # Go to Mechanics list, carve out some space and print the data.
    # Note: still incomplete! See MechanicsList.py
    startRow = 2
    nameField1 = 'Test'
    nameField2 = 'Modifier'
    mechanicsSheet = model.Sheets.getByName('Mechanics Test')
    mechanicsList.generateAction(mechanicsSheet, inputDataArray, inputColors, nameField1, nameField2, startRow)
    # test.testItOut(inputSheet, inputDataArray)


def createConditionalFormatting(**kwargs):
    model = environment.getDocument(**kwargs)
    sheet = model.Sheets.getByName('Mechanics Test')
    resultsSheet = model.Sheets.getByName('Results List')

    # A function that gets data from the Results Sheet
    resultsList = conditionalFormat.getResultsList(resultsSheet)
    resultsListColors = conditionalFormat.getResultsListColors(resultsSheet, resultsList)

    # A function that uses the gathered data and generates the formatting.
    # Note: still incomplete! See conditionalFormat.py
    conditionalFormat.applyConditionalFormatting(sheet, resultsList, resultsListColors)


# Run when executed from the command line.
if __name__ == '__main__':
    generateSingleAction(host='localhost', port=2002)
