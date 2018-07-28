from movelister import messageBox


def masterListProjectionErrorCheck(mda, nameCol):

    if len(mda) <= 2 and mda[1][nameCol] == '':
        messageBox.createMessage('OK', 'Warning:', 'Master Action List seems to be empty. Unable to generate.')
        exit()
