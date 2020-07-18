class MovelisterError(Exception):
    """
    Movelister base error from which all other exceptions are derived from.
    Messages from errors derived from this class are shown automatically to the
    user inside LibreOffice message box UI component.
    """
    pass


class DuplicateError(MovelisterError):
    """
    Raised when duplicate exists.
    """
    pass
