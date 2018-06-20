from movelister import messageBox


def projectionErrorCheck(MDA, nameCol):

    if len(MDA) <= 2 and MDA[1][nameCol] == '':
        messageBox.createMessage('OK', 'Warning:', 'Master Action List seems to be empty. Unable to generate.')
        exit()
