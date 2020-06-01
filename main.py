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

from unohelper import fileUrlToSystemPath

# This will modify path to include movelister module be part of it. This is
# needed because this file is the main entry to the program and it can be
# executed from three different contexts: from command-line, from LibreOffice
# when macros are part of the system files and from LibreOffice when movelister
# source files are packed inside LibreOffice document for release.
if __name__ == '__main__':
        sys.path.append(os.path.join(os.path.dirname('__file__'), 'pythonpath'))
elif __name__ == 'ooo_script_framework': # Name when executed from LibreOffice.
        doc = XSCRIPTCONTEXT.getDocument()
        url = fileUrlToSystemPath('{}/{}'.format(doc.URL,'Scripts/python/pythonpath'))
        sys.path.insert(0, url)

from movelister import error, selection  # noqa
from movelister.core import cursor # noqa
from movelister.core.alignment import HorizontalAlignment, VerticalAlignment # noqa
from movelister.core.context import Context # noqa
from movelister.format import action, color, convert, format, namedRanges, overview, validation # noqa
from movelister.format.details import DetailsFormatter # noqa
from movelister.format.overview import OverviewFormatter # noqa
from movelister.model.action import Action # noqa
from movelister.model.color import Color # noqa
from movelister.process.factory import OverviewFactory # noqa
from movelister.process.updateOverview import UpdateOverview # noqa
from movelister.process.updateDetails import UpdateDetails # noqa
from movelister.sheet import helper # noqa
from movelister.sheet.details import Details # noqa
from movelister.sheet.inputs import Inputs # noqa
from movelister.sheet.master import Master # noqa
from movelister.sheet.modifiers import Modifiers # noqa
from movelister.sheet.overview import Overview # noqa
from movelister.sheet.sheet import Sheet, MASTER_LIST_SHEET_NAME, MODIFIER_LIST_SHEET_NAME # noqa
from movelister.ui import message_box  # noqa

# Setup context automatically when macro is run from the LibreOffice.
if __name__ != '__main__':
    Context.setup()


def updateDetails(*args, **kwargs):
    """
    A macro function that will update one Details sheet while preserving
    previous user data.  The project can have multiple Details-views and which
    one to update is detected from which Overview button was pressed to trigger
    this macro.
    """
    if not error.checkTemplatesExists():
        message_box.showWarningWithOk('This file doesn\'t seem to have all necessary templates. Can\'t generate.')
        return

    # Get overview sheet name from active sheet or from provided kwargs.
    activeOverviewName = kwargs.get('activeSheet', helper.getActiveSheetName())
    # Get view name for the details. This is presented in overview sheet name inside parentheses.
    detailsViewName = re.search('\((.+)\)', activeOverviewName).group(1)
    completeDetailsName = 'Details ({})'.format(detailsViewName)
    previousDetails = Details(detailsViewName)
    if Sheet.hasByName(completeDetailsName):
        # Check if user wants to update existing detail sheet.
        if not message_box.showSheetUpdateWarning():
            return
        previousDetails = Details.fromSheet(completeDetailsName)
    modifiersSheet = Modifiers(MODIFIER_LIST_SHEET_NAME)
    parentOverview = Overview.fromSheet(activeOverviewName)
    # Create new Details sheet by combining new and existing data.
    newDetails = UpdateDetails.update(modifiersSheet, parentOverview, previousDetails, detailsViewName)
    # Delete previous details sheet and generate a new one.
    Sheet.deleteSheetByName(completeDetailsName)
    formatter = DetailsFormatter(newDetails, parentOverview)
    detailsSheet = formatter.generate()
    # Make columns width optimal.
    length = cursor.getColumnLength(detailsSheet)
    format.setOptimalWidthToRange(detailsSheet, 0, length)
    # Generate data validation.
    validation.setDataValidationToDetailsSheet(detailsSheet)


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
    updateDetails(activeSheet='Overview (Default)')
