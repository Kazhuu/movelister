from movelister import messageBox


def overviewProjectionErrorCheck(mda, nameCol):
    if len(mda) <= 2 and mda[1][nameCol] == '':
        msgText = 'Overview seems to be empty. Unable to generate.'
        messageBox.createMessage('OK', 'Warning:', msgText)
        exit()


def listGenerationNameCheck(document, sheetName):
    if document.Sheets.hasByName(sheetName) == True:
        msgText = 'A Sheet of that name already exists. Would you like to update its contents?'
        result = messageBox.createMessage('YES_NO', 'Warning:', msgText)
        if result == 'YES':
            return 'YES'
        else:
            return 'NO'
    else:
        return 'GENERATE'


def impossibleVariationsErrorCheck(mode, loopAmount):
    if mode == 'OR' and loopAmount > 1:
        msgText = 'The Sheet has more than 1 OR rule column. Be aware that this may create faulty results.'
        messageBox.createMessage('OK', 'Warning:', msgText)
