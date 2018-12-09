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
from movelister.sheet import Master # noqa
from movelister.sheet import Modifiers # noqa
from movelister import color, conditionalFormat, details, error, formatting, generate, loop, \
    overview, modifierList, namedRanges, selection, ui, resultsList, text, validation  # noqa

# Setup context automatically when macro is run from the LibreOffice.
if __name__ != '__main__':
    Context.setup()


def setColor():
    """
    Test macro to test Color class and setting color.
    """
    modifierSheet = Sheet.getModifierListSheet()
    c = color.Color(modifierSheet.getCellByPosition(0, 0).CellBackColor)
    c.alpha = 0
    c.red = 0
    c.green = 0
    c.blue = 255
    print(hex(c.value))
    modifierSheet.getCellByPosition(0, 0).CellBackColor = c.value


def generateOrRefreshDetails(*args):
    """
    A very general function that creates / refreshes full Details view up to date with a single button.
    If the project has multiple Details views, there would probably be some drop down menu
    pointing the code to the correct List before the code is ran.
    """
    document = Context.getDocument()
    inputSheet = Sheet.getInputSheet()
    detailsSheet = Sheet.getDetailsSheet()
    modifierSheet = Sheet.getModifierSheet()

    name = text.getActiveSheetView(document)
    sheetName = 'Details (' + name + ')'
    templateName = 'Details Template'

    # A bit of error checking at the start.
    error.generateSheetTemplateCheck(document, templateName)
    result = error.generateSheetNameCheck(document, sheetName)

    if result == 'GENERATE':
        generate.generateSheetFromTemplate(document, templateName, sheetName)
        # The code then segues into the usual "refresh" code that updates the info inside the List.
    elif result == 'YES':
        print()
        # To do: go to Details refresh function.
    elif result == 'NO':
        print('Exiting function...')

    '''
    # The code goes through Overview and makes a "projection" of what the Details sheet should
    # look like. It's a multi-dimensional array where [0] lists action name, [1] lists modifiers, [2] lists
    # input list and [3] lists the expected location of the action in Details list.
    projectionOverview = overview.getOverviewProjection(overviewSheet, modifierSheet, inputSheet)
    print("projektion: " + str(projectionOverview))

    # Same thing for what is currently inside Mechanics List.
    projectionDetails = details.getDetailsSheetProjection(detailsSheet, projectionOverview)

    # Code creates a new Array which is eventually pasted on Details Sheet, replacing it
    # entirely in a single swoop. (It's faster to do it like this than generate row-by-row.)
    details.refreshDetailsSheet(detailsSheet, inputSheet, projectionOverview, projectionDetails)

    # TO DO: regenerate conditional formatting.
    # TO DO: color cell backgrounds according to info. There are basically three types of coloring:
    # action colors, modifier colors and input colors.
    actionColors = loop.getColorArray(overviewSheet)
    modifierColors = loop.getColorArray(modifierSheet)
    inputColors = loop.getColorArray(inputSheet)

    formatting.setDetailsSheetColors(detailsSheet, actionColors, modifierColors, inputColors)
    '''

    # TO DO: group rows according to info in Input List.


def generateOrRefreshOverview(*args):
    document = Context.getDocument()
    masterSheet = Sheet.getMasterSheet()

    # Get the name of the Overview that is generated or refreshed.
    target = masterSheet.getCellByPosition(2, 0).getString()
    sheetName = 'Overview (' + target + ')'
    templateName = 'Overview Template'

    # A bit of error checking at the start.
    error.generateSheetTemplateCheck(document, templateName)
    result = error.generateSheetNameCheck(document, sheetName)

    if result == 'GENERATE':
        generate.generateSheetFromTemplate(document, templateName, sheetName)
    elif result == 'YES':
        print()
        # To do: go to Overview refresh function.
    else:
        print('Exiting function...')

    # How to define the position of the new document? Group it with other Overviews?
    # Leave it up to the user to move it?


def selectionTest():
    """
    A quick test for getting active Selection from the sheet.
    """
    selectionA = selection.getCurrentSelection()
    result = selection.determineSelectionType(selectionA)
    print(result)


def namedRangeTest():
    """
    Quick tests with named ranges.
    """
    detailsSheet = Sheet.getDetailsSheet()
    namedRange = Context.getDocument().NamedRanges
    namedRanges.deleteNamedRanges(namedRange)
    namedRanges.createNewNamedRange(detailsSheet, namedRange)


def generateButtonTest():
    """
    Quick test with generating a button.
    """
    overviewSheet = Sheet.getOverviewSheet()

    buttonModel = ui.generateButton(overviewSheet, 'Button', 'Jee', 200, 400, 5000, 1000)

    # TO DO: adding event listener to button still doesn't work.
    ui.addEventListenerToButton(buttonModel)


def refreshPhases():
    """
    Old code...

    A test function for removing or adding phases in Mechanics List. Seems to work,
    but the code could probably be more elegant.
    """
    overviewSheet = Sheet.getOverviewSheet()
    detailsSheet = Sheet.getDetailsSheet()

    # A function that fetches the highest phase number in Overview.
    # To do: to be more flexible, the code should also take into account if the high phase numbers
    # are actually USED at all in the Mechanics List.
    masterDataArray = overview.getOverview(overviewSheet)
    highestPhase = overview.getHighestPhaseNumber(overviewSheet, len(masterDataArray))

    # A function that counts the phases in the Details Sheet.
    phaseCount = details.countPhases(detailsSheet)

    # Comparing the highest known Phase number in Overview vs Details Sheet phase number
    # and determining if new phases have to be added or deleted.
    if highestPhase == phaseCount:
        print('No need to add or delete phases.')
    if highestPhase > phaseCount:
        details.generatePhases(detailsSheet, highestPhase, phaseCount)
    if highestPhase < phaseCount:
        details.deletePhases(detailsSheet, highestPhase, phaseCount)

    # To do: a function may have to re-generate Conditional Formatting for the sheet.


def refreshModifiers():
    """
    A function that refreshes the modifier block of Overview based on the data
    the user has set inside Modifier List. This includes the number and position of
    various modifiers as well as their color.
    """
    overviewSheet = Sheet.getByName('Overview (Default)')
    modifierSheet = Sheet.getByName('Modifier List')

    # Getting the list of modifiers from a chosen Overview.
    overviewModifiers = overview.getOverviewModifiers(overviewSheet)

    # Getting the list of modifiers from the Modifiers list.
    # A separate array is created for the cell background color data.
    modifierListModifiers = modifierList.getModifierListProjection(modifierSheet)
    modifierColors = loop.getColorArray(modifierSheet)

    # Compare if Overview modifiers match Modifier List modifiers. Returns False if the two lists are different.
    result = error.compareModifierLists(modifierListModifiers, overviewModifiers)

    # Function compares this data to the Modifiers columns in an Overview.
    # It then deletes unnecessary Modifier columns or add necessary Modifier Columns in the Overview.
    # It then colors the cell background of the columns.
    if result is False:
        overview.updateOverviewModifiers(overviewSheet, overviewModifiers, modifierListModifiers, modifierColors)


def createConditionalFormatting():
    """
    A test function for just setting up quick conditional formatting.
    """
    detailsSheet = Sheet.getDetailsSheet()
    resultsSheet = Sheet.getResultSheet()

    # A function that gets all relevant data from the Results Sheet.
    resultsDataArray = resultsList.getResultsList(resultsSheet)
    resultsColors = loop.getColorArray(resultsSheet)

    # A function that uses the gathered data and generates the formatting.
    # Note: still incomplete! See conditionalFormat.py
    conditionalFormat.applyConditionalFormatting(detailsSheet, resultsDataArray, resultsColors)
    # conditionalFormat.clearConditionalFormatting(detailsSheet)


def createValidation():
    """
    A test function for creating some data validation.
    """
    sheet = Sheet.getByName('Overview Template')
    validation.setDataValidationToColumn(sheet, 3, 'phase')


def testingClasses():
    masterList = Master('Master List')
    actions = masterList.getActions('Default')

    modifierList = Modifiers('Modifier List')
    modifiers = modifierList.getModifiers()

    for row in actions:
        print(row.name)

    for row in modifiers:
        print(row)


# Run when executed from the command line.
if __name__ == '__main__':
    Context.setup(host='localhost', port=2002)
    testingClasses()
