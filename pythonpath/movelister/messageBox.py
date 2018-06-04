from com.sun.star.awt import MessageBoxType
from com.sun.star.awt import MessageBoxButtons
from com.sun.star.awt import MessageBoxResults

from movelister.context import Context


def createMessage(type, titleText, messageText):
    model = Context.getDocument()
    window = model.CurrentController.Frame.ContainerWindow

    if type == 'OK':
        box = window.getToolkit().createMessageBox(
            window, MessageBoxType.MESSAGEBOX,
            MessageBoxButtons.BUTTONS_OK, titleText, messageText)
    if type == 'YES_NO':
        box = window.getToolkit().createMessageBox(
            window, MessageBoxType.MESSAGEBOX,
            MessageBoxButtons.BUTTONS_YES_NO, titleText, messageText)

    result = box.execute()
    if result == MessageBoxResults.OK:
        return 'OK'
    if result == MessageBoxButtons.YES:
        return 'YES'
    if result == MessageBoxButtons.NO:
        return 'NO'
