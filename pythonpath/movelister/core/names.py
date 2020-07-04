import re


def getViewName(sheetName):
    """
    Return view name from the given sheet name. View name is presented inside
    parenthesis. For instance 'Details (Default)' where 'Default' is a view name
    which is returned.
    """
    return re.search('\((.+)\)', sheetName).group(1)


def getDetailsName(viewName):
    """
    Return Details sheet name formatted with given view.
    """
    return 'Details ({})'.format(viewName)


def getOverviewName(viewName):
    """
    Return Overview sheet name formatted with given view.
    """
    return 'Overview ({})'.format(viewName)
