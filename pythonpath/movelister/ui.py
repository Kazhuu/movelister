import uno
import unohelper

from com.sun.star.awt import XActionListener
from movelister.core import Context


class MyActionListener(unohelper.Base, XActionListener):

    def __init__(self):
        print("ok1")

    def actionPerformed(self, actionEvent):
        print("ok2")


def generateButton(sheet, name, label, positionX, positionY, sizeWidth, sizeHeight):
    """
    A function that generates a button to a sheet. Event Listener is added separately.
    """
    document = Context.getDocument()
    services = Context.getServiceManager()
    context = Context.getContext()

    shape = document.createInstance("com.sun.star.drawing.ControlShape")
    point = uno.createUnoStruct('com.sun.star.awt.Point')
    size = uno.createUnoStruct('com.sun.star.awt.Size')
    point.X = positionX
    point.Y = positionY
    size.Width = sizeWidth
    size.Height = sizeHeight
    shape.setPosition(point)
    shape.setSize(size)

    buttonModel = services.createInstanceWithContext("com.sun.star.form.component.CommandButton", context)
    buttonModel.Name = name
    buttonModel.Label = label

    shape.setControl(buttonModel)

    drawPage = sheet.DrawPage
    drawPage.add(shape)

    aEvent = uno.createUnoStruct("com.sun.star.script.ScriptEventDescriptor")
    aEvent.AddListenerParam = ""
    aEvent.EventMethod = "actionPerformed"
    aEvent.ListenerType = "XActionListener"
    aEvent.ScriptCode = "movelister|main.py$generateOrRefreshMechanicsList (share, Python)"
    aEvent.ScriptType = "Script"

    oForm = drawPage.getForms().getByIndex(0)
    oForm.getCount()
    oForm.registerScriptEvent(0, aEvent)

    return buttonModel


def addEventListenerToButton(button):
    pass
    # To do: code doesn't work on each run?
    # To do: does the actionlistener even work on the button?

    # document = Context.getDocument()
    # controller = document.getCurrentController()

    # print(controller)

    # listener = MyActionListener()

    # button.addActionListener(listener)

    # controller.getControl(button).addActionListener(listener)
