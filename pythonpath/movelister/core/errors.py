from movelister.sheet.sheet import Sheet


class MovelisterError(Exception):
    """
    Movelister base error from which all other exceptions are derived from.
    Messages from errors derived from this class are shown automatically to the
    user inside LibreOffice message box UI component.

    After displaying the error given sheet name will be set as currently
    active sheet. This will point user straight to the sheet where error
    is.
    """
    def __init__(self, activeSheetName, message):
        Exception.__init__(self, message)
        self.activeSheet = Sheet.getByName(activeSheetName)


class DuplicateError(MovelisterError):
    """
    Raised when duplicate exists.
    """
    pass


class UnsupportedCharacter(MovelisterError):
    """
    Raised when string contains unsupported characters.
    """
    pass
