from com.sun.star.awt.MessageBoxType import MESSAGEBOX, INFOBOX, WARNINGBOX, ERRORBOX, QUERYBOX
from com.sun.star.awt.MessageBoxButtons import BUTTONS_OK, BUTTONS_OK_CANCEL, BUTTONS_YES_NO, \
 BUTTONS_YES_NO_CANCEL, BUTTONS_RETRY_CANCEL, BUTTONS_ABORT_IGNORE_RETRY
from com.sun.star.awt.MessageBoxResults import OK, YES, NO, CANCEL

from movelister import environment


def createMessage(type, titleText, messageText, **kwargs):
    model = environment.getDocument(**kwargs)
    window = model.CurrentController.Frame.ContainerWindow

    if type == 'OK':
        box = window.getToolkit().createMessageBox(window, MESSAGEBOX,  BUTTONS_OK, titleText, messageText)
    if type == 'YES_NO':
        box = window.getToolkit().createMessageBox(window, MESSAGEBOX,  BUTTONS_YES_NO, titleText, messageText)

    result = box.execute()
    if result == OK:
        return 'OK'
    if result == YES:
        return 'YES'
    if result == NO:
        return 'NO'
