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

from movelister.core import HorizontalAlignment, VerticalAlignment, Context, cursor # noqa
from movelister.format import autofill, color, convert, format, namedRanges, overview, OverviewFormatter, validation # noqa
from movelister.format import OverviewFormatter  # noqa
from movelister.model import Color # noqa
from movelister.process import OverviewFactory, UpdateOverview # noqa
from movelister.sheet import helper, Inputs, Master, Modifiers, Overview, Sheet # noqa
from movelister import error, selection  # noqa
from movelister.sheet import Master, MASTER_LIST_SHEET_NAME, MODIFIER_LIST_SHEET_NAME  # noqa
from movelister.ui import message_box  # noqa

# Setup context automatically when macro is run from the LibreOffice.
if __name__ != '__main__':
    Context.setup()


def generateOrRefreshDetails(*args):
    """
    A very general function that creates / refreshes full Details view up to date with a single button.
    The project can have multiple Details-views and the user directs the code to the correct one with
    a name in the Overview-sheet.
    """
    document = Context.getDocument()

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
    # TODO: adjust wideness of the Details-view based on maximum number of phases?
    # TODO: color cell backgrounds with conditional formatting.
    # TODO: group rows according to info in Input List?
    # TODO: create a named range of all Actions in Details-view?
    '''


def generateOrRefreshOverview(*args):
    if not error.checkTemplatesExists():
        message_box.showWarningWithOk('This file doesn\'t seem to have all necessary templates. Can\'t generate.')
        return

    # Get name of the overview which user wants to generate.
    masterSheet = Master(MASTER_LIST_SHEET_NAME)
    overviewName = masterSheet.getOverviewName()
    completeOverviewName = 'Overview ({})'.format(overviewName)

    if not overviewName:
        message_box.showWarningWithOk('Provide overview name to generate or refresh')
        return

    if Sheet.hasByName(completeOverviewName):
        # Check if user wants to update existing overview.
        if not message_box.showSheetUpdateWarning():
            return
        oldOverview = Overview.fromSheet(completeOverviewName)
        newOverview = UpdateOverview.update(oldOverview, overviewName)
    else:
        newOverview = Overview(overviewName)

    # Delete old sheet.
    Sheet.deleteSheetByName(completeOverviewName)
    # Generate a new one.
    formatter = OverviewFormatter(newOverview)
    overviewSheet = formatter.generate()
    # Make columns width optimal.
    length = cursor.getColumLength(overviewSheet)
    format.setOptimalWidthToRange(overviewSheet, 0, length)


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
    actions = masterList.getActions('Default')

    modifierList = Modifiers('Modifiers')
    modifiers = modifierList.getModifiers()

    inputList = Inputs('Inputs')
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
    format.setHorizontalAlignmentToRange(masterSheet, HorizontalAlignment.RIGHT, 1, 4)
    format.setVerticalAlignmentToRange(masterSheet, VerticalAlignment.CENTER, 1, 10, 20, 25)
    c = color.getTitleBarColor(aboutSheet)

    range = masterSheet.getCellRangeByPosition(1, 1, 4, 4)
    color.setColorToRange(c, range)


def testingModifiers():
    overview = Overview.fromSheet('Overview (Default)')
    overviewFormat = OverviewFormatter(overview)

    masterList = Master('Master List')
    modifierList = Modifiers('Modifiers')

    # factory = OverviewFactory()
    # testOverview = factory.createOverview(masterList, 'Default')

    overviewFormat.setOverviewModifierColors()

    for a in overviewFormat.instance.modifiers:
        print(a.color)


# Run when executed from the command line.
if __name__ == '__main__':
    Context.setup(host='localhost', port=2002)
    testingFormatting()
