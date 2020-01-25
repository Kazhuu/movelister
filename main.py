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
from movelister.format import autofill, color, convert, format, namedRanges, overview, OverviewFormatter, action, validation # noqa
from movelister.model import Action, Color # noqa
from movelister.process import OverviewFactory, UpdateOverview # noqa
from movelister.sheet import Details, helper, Inputs, Master, Modifiers, Overview, Sheet # noqa
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
    if not error.checkTemplatesExists():
        message_box.showWarningWithOk('This file doesn\'t seem to have all necessary templates. Can\'t generate.')
        return

    # Get name of the Details which user wants to generate.
    # TO DO: the code for Details refreshing can be driven from Master sheet or Overview itself.
    # The code should take that into account instead of just using the name from Master list.
    masterSheet = Master(MASTER_LIST_SHEET_NAME)
    detailsName = masterSheet.getOverviewName()
    completeDetailsName = 'Details ({})'.format(detailsName)

    if not detailsName:
        message_box.showWarningWithOk('Provide Details name to generate or refresh.')
        return

    details = Details.fromSheet(completeDetailsName)

    # document = Context.getDocument()
    # activeSheet = helper.getActiveSheet(document)

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

    # Get name of the Overview which user wants to generate.
    masterSheet = Master(MASTER_LIST_SHEET_NAME)
    overviewName = masterSheet.getOverviewName()
    completeOverviewName = 'Overview ({})'.format(overviewName)

    if not overviewName:
        message_box.showWarningWithOk('Provide Overview name to generate or refresh.')
        return

    oldOverview = Overview(overviewName)
    # If document has existing Overview, then that is set as previous instead.
    if Sheet.hasByName(completeOverviewName):
        # Check if user wants to update existing Overview.
        if not message_box.showSheetUpdateWarning():
            return
        oldOverview = Overview.fromSheet(completeOverviewName)

    newOverview = UpdateOverview.update(oldOverview, overviewName)

    # Delete old sheet if exist.
    Sheet.deleteSheetByName(completeOverviewName)
    # Generate a new one.
    formatter = OverviewFormatter(newOverview)
    overviewSheet = formatter.generate()
    # Make columns width optimal.
    length = cursor.getColumnLength(overviewSheet)
    format.setOptimalWidthToRange(overviewSheet, 0, length)
    # Fix sheet colors.
    formatter.setOverviewModifierColors(completeOverviewName)
    formatter.setOverviewActionColors(completeOverviewName)


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
    generateOrRefreshDetails()
