import uno


def getDesktop(host='localhost', port=2002):
    try:
        return XSCRIPTCONTEXT.getDesktop()
    except NameError:
        # Get the uno component context from the PyUNO runtime.
        localContext = uno.getComponentContext()
        # Create the UnoUrlResolver with context.
        resolver = localContext.ServiceManager.createInstanceWithContext(
            'com.sun.star.bridge.UnoUrlResolver', localContext)
        # Connect to the running office.
        uri = 'uno:socket,host={0},port={1};urp;StarOffice.ComponentContext'.format(host, port)
        ctx = resolver.resolve(uri)
        manager = ctx.ServiceManager
        # Get the central desktop object.
        return manager.createInstanceWithContext('com.sun.star.frame.Desktop', ctx)


def getModel(desktop=None, **kwargs):
    if desktop is None:
        return getDesktop(**kwargs).getCurrentComponent()
    return desktop.getCurrentComponent()
