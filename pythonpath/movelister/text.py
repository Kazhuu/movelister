from movelister import error


def getActiveSheetView(document):
    '''
    This function splices the string between () from the current active sheet.
    Used in generating Details view.
    '''
    activeSheet = document.getCurrentController().getActiveSheet()
    activeSheetName = activeSheet.Name

    # A bit of error checking.
    error.sheetNameSplitCheck(activeSheetName)

    splitName1 = activeSheetName.split('(')
    splitName2 = splitName1[1].split(')')

    return splitName2[0]
