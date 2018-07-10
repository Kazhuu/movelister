from movelister import cursor


def getResultsList(resultsSheet):
    resultsDataArray = cursor.getSheetContent(resultsSheet)

    return resultsDataArray
