"""
Main entry file for the whole project for both LibreOffice UI and a command-line interface.

For LibreOffice this file contains all runnable Python macros which can be
attached to key combinations or buttons on the sheet. For command-line
interface this file will connect to a running LibreOffice process using socket
and execute this file as a normal Python script. The command-line interface is
mainly useful during the development. It enables running and debugging macros
from the command-line without using LibreOffice.
"""
import uno # noqa
import os
import sys
import re

# This is to emulate how LibreOffice adds pythonpath folder to PYTHONPATH where
# the script is executed. PYTHONPATH is added when executing from the command
# line.
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname('__file__'), 'pythonpath'))

from movelister.core import HorizontalAlignment, VerticalAlignment, Context, cursor # noqa
from movelister.format import color, convert, format, namedRanges, overview, OverviewFormatter, DetailsFormatter, action, validation # noqa
from movelister.model import Action, Color # noqa
from movelister.process import OverviewFactory, UpdateOverview # noqa
from movelister.process.updateDetails import UpdateDetails
from movelister.sheet import Details, helper, Inputs, Master, Modifiers, Overview, Sheet # noqa
from movelister import error, selection  # noqa
from movelister.sheet import Master, MASTER_LIST_SHEET_NAME, MODIFIER_LIST_SHEET_NAME  # noqa
from movelister.ui import message_box  # noqa

# Setup context automatically when macro is run from the LibreOffice.
if __name__ != '__main__':
    Context.setup()


def updateDetails(*args):
    """
    A macro function that will update one Details sheet while preserving
    previous user data.  The project can have multiple Details-views and which
    one to update is detected from which Overview button was pressed to trigger
    this macro.
    """
    if not error.checkTemplatesExists():
        message_box.showWarningWithOk('This file doesn\'t seem to have all necessary templates. Can\'t generate.')
        return

    # Get overview sheet name if provided or from sheet where button was pressed.
    activeOverviewName = ''
    if len(args) > 0:
        activeOverviewName = args[0]
    else:
        activeOverviewName = helper.getActiveSheetName()
    # Get view name for the details. This is presented in overview sheet name inside parentheses.
    detailsViewName = re.search('\((.+)\)', activeOverviewName).group(1)
    completeDetailsName = 'Details ({})'.format(detailsViewName)
    previousDetails = Details(detailsViewName)
    if Sheet.hasByName(completeDetailsName):
        # Check if user wants to update existing detail sheet.
        if not message_box.showSheetUpdateWarning():
            return
        previousDetails = Details.fromSheet(completeDetailsName)
    newDetails = UpdateDetails.update(previousDetails, detailsViewName)
    # Delete previous details sheet and generate a new one.
    Sheet.deleteSheetByName(completeDetailsName)
    formatter = DetailsFormatter(newDetails)
    detailsSheet = formatter.generate()


def updateOverview(*args):
    """
    A macro function to update or create a new Overview sheet. Updated sheet
    will include earlier user data in the old Overview if any.
    """
    if not error.checkTemplatesExists():
        message_box.showWarningWithOk('This file doesn\'t seem to have all necessary templates. Can\'t generate.')
        return

    # Get name of the Overview which user wants to generate.
    masterSheet = Master(MASTER_LIST_SHEET_NAME)
    overviewName = masterSheet.getOverviewName()
    completeOverviewName = 'Overview ({})'.format(overviewName)

    if not overviewName:
        message_box.showWarningWithOk('Provide Overview name to update.')
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


# Run this when executed from the command line.
if __name__ == '__main__':
    Context.setup(host='localhost', port=2002)
    updateDetails('Overview (Default)')
