import os
import sys

import uno


def python_version(*args):
    """
    Prints the Python version into the current document
    """
    # Get the doc from the scripting context which is made available to all scripts
    desktop = XSCRIPTCONTEXT.getDesktop()
    model = desktop.getCurrentComponent()
    # Check whether there's already an opened document. Otherwise, create a new one
    if not hasattr(model, "Text"):
        model = desktop.loadComponentFromURL("private:factory/swriter", "_blank", 0, ())
    # Get the XText interface
    text = model.Text
    # Create an XTextRange at the end of the document
    tRange = text.End
    # And set the string
    tRange.String = "The Python version is %s.%s.%s" % sys.version_info[:3] + " and the executable path is "
    + sys.executable
    return None


def working_directory():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)


def python_executable_path():
    print(sys.executable)


def pythonpath():
    print(sys.path)


def kappa(*args):
    desktop = XSCRIPTCONTEXT.getDesktop()
    model = desktop.getCurrentComponent()
    model.Sheets.insertNewByName("Nojes", 0)
    newSheet = model.Sheets.getByName("Nojes")
    newSheet.getCellByPosition(0, 0).setString("Test")
    a = 1
    testCell = newSheet.getCellByPosition(1, 1)
    testCell.setString(a)
    return None
