from movelister import messageBox


def masterListProjectionErrorCheck(mda, nameCol):

    if len(mda) <= 2 and mda[1][nameCol] == '':
        messageBox.createMessage('OK', 'Warning:', 'Master Action List seems to be empty. Unable to generate.')
        exit()


def impossibleVariationsErrorCheck(mode, loopAmount):
    if mode == 'OR' and loopAmount > 1:
        messageBox.createMessage('OK', 'Warning:', 'The Sheet has more than 1 OR rule column. Be aware that this may \
                                 create faulty results.')
