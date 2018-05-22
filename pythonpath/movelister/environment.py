import uno

from com.sun.star.connection import NoConnectException


def getDesktop(**kwargs):
    """
    Returns Desktop UNO object by abstracting executable environment.
    If host and port parameters are given, then socket connections is used.
    Otherwise Desktop object is created using LibreOffice runtime process.
    """
    # Get the uno component context from the PyUNO runtime.
    context = uno.getComponentContext()
    if 'host' in kwargs and 'port' in kwargs:
        try:
            # Create the UnoUrlResolver with context.
            resolver = context.ServiceManager.createInstanceWithContext(
                'com.sun.star.bridge.UnoUrlResolver', context)
            # Connect to the running office.
            uri = 'uno:socket,host={0},port={1};urp;StarOffice.ComponentContext'.format(kwargs['host'], kwargs['port'])
            context = resolver.resolve(uri)
            manager = context.ServiceManager
            # Get the central desktop object.
            return manager.createInstanceWithContext('com.sun.star.frame.Desktop', context)
        except NoConnectException:
            print('could not connect to LibreOffice socket at {0}:{1}'.format(kwargs['host'], kwargs['port']))
            print('make sure the socket is open')
            return None
    else:
        desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
        return desktop


def getDocument(desktop=None, **kwargs):
    """
    Returns current document component by abstracting executable enviroment.
    """
    if desktop is None:
        return getDesktop(**kwargs).getCurrentComponent()
    return desktop.getCurrentComponent()