from movelister.ui import messageBox


def overviewProjectionErrorCheck(mda, nameCol):
    if len(mda) <= 2 and mda[1][nameCol] == '':
        msgText = 'Overview seems to be empty. Unable to generate.'
        messageBox.createMessage('OK', 'Warning:', msgText)
        exit()


def generateSheetNameCheck(document, sheetName):
    if document.Sheets.hasByName(sheetName) is True:
        msgText = 'A Sheet of that name already exists. Would you like to update its contents?'
        result = messageBox.createMessage('YES_NO', 'Warning:', msgText)
        if result == 'YES':
            return 'YES'
        else:
            return 'NO'
    else:
        return 'GENERATE'


def generateSheetTemplateCheck(document, templateName):
    if document.Sheets.hasByName(templateName) is False:
        msgText = 'This file doesn\'t seem to have all necessary templates. Can\'t generate.'
        messageBox.createMessage('OK', 'Warning:', msgText)
        exit()


def sheetNameSplitCheck(name):
    if '(' not in name or ')' not in name:
        msgText = 'The active sheet name lacks parentheses.'
        messageBox.createMessage('OK', 'Warning:', msgText)
        exit()


def impossibleVariationsErrorCheck(mode, loopAmount):
    if mode == 'OR' and loopAmount > 1:
        msgText = 'The Sheet has more than 1 OR rule column. Be aware that this may create faulty results.'
        messageBox.createMessage('OK', 'Warning:', msgText)


def compareModifierLists(modifierListModifiers, overviewModifiers):
    """
    This function compares both modifier lists. If they're identical, returns True.
    """

    if modifierListModifiers == overviewModifiers:
        messageBox.createMessage('OK', "Note:", "Modifier lists are already up to date.")
        return True
    else:
        return False
