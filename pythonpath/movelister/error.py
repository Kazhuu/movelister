from movelister.ui import message_box
from movelister.sheet.sheet import Sheet


def overviewProjectionErrorCheck(mda, nameCol):
    if len(mda) <= 2 and mda[1][nameCol] == '':
        msgText = 'Overview seems to be empty. Unable to generate.'
        message_box.createMessage('OK', 'Warning:', msgText)
        exit()


def checkTemplatesExists():
    """
    Return true if all needed template sheets exists for this document, false otherwise.
    """
    return Sheet.hasByName('Overview Template') and Sheet.hasByName('Details Template')


def compareModifierLists(modifierListModifiers, overviewModifiers):
    """
    This function compares both modifier lists. If they're identical, returns True.
    """

    if modifierListModifiers == overviewModifiers:
        message_box.createMessage('OK', "Note:", "Modifier lists are already up to date.")
        return True
    else:
        return False
