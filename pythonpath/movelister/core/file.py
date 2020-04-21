from movelister.core.context import Context


def reopenCurrentFile():
    """
    Reopens current file. All variables made before this will be
    invalid. Make sure to initialize them too.
    """
    frame = Context.getFrame()
    frame.loadComponentFromURL(getUrl(), "_self", 0, ())


def getUrl():
    """
    Returns current opened file URL. This can be used to reopen the
    same file. URL format for a file is:
    "file:///path_to_project/movelister/templates/movelister_template.ods"
    """
    return Context.getFrame().getController().getModel().getURL()
