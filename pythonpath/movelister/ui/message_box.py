from com.sun.star.awt.MessageBoxType import MESSAGEBOX
from com.sun.star.awt import MessageBoxButtons
from com.sun.star.awt import MessageBoxResults

from movelister.core import Context


def createMessage(type, titleText, messageText):
    model = Context.getDocument()
    window = model.CurrentController.Frame.ContainerWindow

    if type == 'OK':
        box = window.getToolkit().createMessageBox(
            window, MESSAGEBOX,
            MessageBoxButtons.BUTTONS_OK, titleText, messageText)
    if type == 'YES_NO':
        box = window.getToolkit().createMessageBox(
            window, MESSAGEBOX,
            MessageBoxButtons.BUTTONS_YES_NO, titleText, messageText)

    result = box.execute()
    if result == MessageBoxResults.OK:
        return 'OK'
    if result == MessageBoxResults.YES:
        return 'YES'
    if result == MessageBoxResults.NO:
        return 'NO'
