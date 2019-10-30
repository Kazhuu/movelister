"""
Main file for the all usable LibreOffice macros. Can also be executed from the
command line and connect to opened LibreOffice socket.
"""
import uno # noqa
import os
import sys

# This is to emulate how LibreOffice adds pythonpath folder to PYTHONPATH where
# the script is executed. PYTHONPATH is added when executing from the command
# line.
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname('__file__'), 'pythonpath'))

from movelister.core import Alignment, Context, cursor # noqa
from movelister.format import autofill, color, format, namedRanges, overview, OverviewFormatter, validation # noqa
from movelister.model import Color # noqa
from movelister.process import OverviewFactory # noqa
from movelister.sheet import helper, Inputs, Master, Modifiers, Overview, Sheet # noqa
from movelister import conditionalFormat, details, error, overview, modifierList, selection, ui  # noqa

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
    # inputSheet = Sheet.getInputSheet()
    # detailsSheet = Sheet.getDetailsSheet()
    # modifierSheet = Sheet.getModifierSheet()

    activeSheet = helper.getActiveSheet(document)
    error.sheetNameSplitCheck(activeSheet.Name)
    name = helper.getViewName(activeSheet.Name)

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
    actionColors = helper.getColorArray(overviewSheet)
    modifierColors = helper.getColorArray(modifierSheet)
    inputColors = helper.getColorArray(inputSheet)

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


def namedRangeTest():
    """
    Quick tests with named ranges.
    """
    document = Context.getDocument()
    activeSheet = helper.getActiveSheet(document)

    namedRange = Context.getDocument().NamedRanges
    namedRanges.deleteNamedRanges(namedRange)
    namedRanges.createNewNamedRange(activeSheet, namedRange)


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


def refreshModifiers(args):
    """
    A function that refreshes the modifier block of Overview based on the data
    the user has set inside Modifier List. This includes the number and position of
    various modifiers as well as their color.

    This code is always ran through the 'Refresh'-button on the Overview Template,
    so it expects the active sheet to be one of the Overviews.
    """
    document = Context.getDocument()
    activeSheet = helper.getActiveSheet(document)

    sheetName = 'Overview (' + helper.getViewName(activeSheet.Name) + ')'
    overview = Overview.fromSheet(sheetName)

    modifiers = Modifiers("Modifiers").getModifiers()

    if overview.modifiers == modifiers:
        print('Modifiers are already up to date in this Overview.')
        exit()

    # Getting the list of modifiers from a chosen Overview.
    # overviewModifiers = overview.getOverviewModifiers(overviewModifierData)

    # Getting the list of modifiers from the Modifier list.


    # Compare if Overview modifiers match Modifier List modifiers. Returns False if the two lists are different.
    # result = error.compareModifierLists(modifierListModifiers, overviewModifiers)

    # Function compares this data to the Modifiers columns in an Overview.
    # It then deletes unnecessary Modifier columns or add necessary Modifier Columns in the Overview.
    # It then colors the cell background of the columns.
    # if result is False:
    # overview.updateOverviewModifiers(overviewSheet, overviewModifiers, modifierListModifiers, modifierColors)


def createValidation():
    """
    A test function for creating some data validation.
    """
    sheet = Sheet.getByName('Overview Template')
    validation.setDataValidationToColumn(sheet, 3, 'phase')


def testingClasses():
    masterList = Master('Master List')
    autofill.autoFillMasterList(masterList)
    actions = masterList.getActions('Default')

    modifierList = Modifiers('Modifiers')
    modifiers = modifierList.getModifiers()

    inputList = Inputs('Inputs')
    autofill.generateDefaultInputs(inputList)
    autofill.autoFillInputs(inputList)
    inputs = inputList.getInputs('Default')

    overviewSheet = Overview('Overview (Default)')
    # Overview still WIP

    for row in actions:
        print(row.__dict__)

    for row in modifiers:
        print(row.__dict__)

    for row in inputs:
        print(row.__dict__)


def testingFormatting():
    masterSheet = Sheet.getByName('Master List')
    aboutSheet = Sheet.getByName('About')
    format.setHorizontalAlignmentToRange(masterSheet, Alignment.RIGHT, 1, 4)
    c = color.getTitleBarColor(aboutSheet)

    range = masterSheet.getCellRangeByPosition(1, 1, 4, 4)
    color.setColorToRange(c, range)


def testingModifiers():
    overview = Overview.fromSheet('Overview (Default)')
    overviewFormat = OverviewFormatter(overview)

    masterList = Master('Master List')
    modifierList = Modifiers('Modifiers')

    overviewSheet = Sheet.getByName('Overview (Default)')
    masterSheet = Sheet.getByName('Master List')

    # factory = OverviewFactory()
    # testOverview = factory.createOverview(masterList, 'Default')

    overviewFormat.setOverviewModifierColors()

    for a in overviewFormat.instance.modifiers:
        print(a.color)


# Run when executed from the command line.
if __name__ == '__main__':
    Context.setup(host='localhost', port=2002)
    namedRangeTest()
