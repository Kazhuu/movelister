from movelister.ui import message_box


def overviewProjectionErrorCheck(mda, nameCol):
    if len(mda) <= 2 and mda[1][nameCol] == '':
        msgText = 'Overview seems to be empty. Unable to generate.'
        message_box.createMessage('OK', 'Warning:', msgText)
        exit()


def generateSheetTemplateCheck(document, templateName):
    if document.Sheets.hasByName(templateName) is False:
        msgText = 'This file doesn\'t seem to have all necessary templates. Can\'t generate.'
        message_box.createMessage('OK', 'Warning:', msgText)
        exit()


def sheetNameSplitCheck(name):
    if '(' not in name or ')' not in name:
        msgText = 'The active sheet name lacks parentheses.'
        message_box.createMessage('OK', 'Warning:', msgText)
        exit()


def impossibleVariationsErrorCheck(mode, loopAmount):
    if mode == 'OR' and loopAmount > 1:
        msgText = 'The Sheet has more than 1 OR rule column. Be aware that this may create faulty results.'
        message_box.createMessage('OK', 'Warning:', msgText)


def compareModifierLists(modifierListModifiers, overviewModifiers):
    """
    This function compares both modifier lists. If they're identical, returns True.
    """

    if modifierListModifiers == overviewModifiers:
        message_box.createMessage('OK', "Note:", "Modifier lists are already up to date.")
        return True
    else:
        return False
