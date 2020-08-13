import uno
from com.sun.star.connection import NoConnectException

from .meta import Singleton


class Context(Singleton):

    EXCEPTION_MESSAGE = 'setup runtime with Context.setup() method before doing anything else'

    @classmethod
    def setup(cls, **kwargs):
        """
        Setups the runtime environment. Must be the first thing to run before
        any other method or function call.
        If host and port parameters are given, then socket connections is used.
        Otherwise context object is created using LibreOffice runtime process.
        """
        if not hasattr(cls, 'desktop'):
            # Get the uno component context from the PyUNO runtime.
            cls.context = uno.getComponentContext()
            if 'host' in kwargs and 'port' in kwargs:
                try:
                    # Create the UnoUrlResolver with context.
                    cls.resolver = cls.context.ServiceManager.createInstanceWithContext(
                        'com.sun.star.bridge.UnoUrlResolver', cls.context)
                    # Connect to the running office.
                    uri = 'uno:socket,host={0},port={1};urp;StarOffice.ComponentContext'.format(
                        kwargs['host'], kwargs['port']
                    )
                    cls.context = cls.resolver.resolve(uri)
                    cls.serviceManager = cls.context.ServiceManager
                    # Get the central desktop object.
                    cls.desktop = cls.serviceManager.createInstanceWithContext(
                        'com.sun.star.frame.Desktop', cls.context)
                    print('connected to port {0} successfully'.format(kwargs['port']))
                except NoConnectException:
                    print('could not connect to LibreOffice socket at {0}:{1}'.format(kwargs['host'], kwargs['port']))
                    print('make sure the socket is open')
                    return None
            else:
                cls.desktop = cls.context.ServiceManager.createInstanceWithContext(
                    "com.sun.star.frame.Desktop", cls.context
                )

    @classmethod
    def reset(cls):
        """
        Resets the current context setup by setup() method. Remember to call
        setup() again after this. This can be used to reset context if LibreOffice
        process has restarted. Useful for unit tests.
        """
        if hasattr(cls, 'desktop'):
            del cls.desktop

    @classmethod
    def getFrame(cls):
        """
        Returns current frame object. RunTimeError is raised if setup() is not called
        before this. Frame represents current active LibreOffice UI.
        """
        return cls.getDesktop().CurrentFrame

    @classmethod
    def getDesktop(cls):
        """
        Returns desktop object. RunTimeError is raised if setup() is not called
        before this.
        """
        if not hasattr(cls, 'desktop'):
            raise RuntimeError(cls.EXCEPTION_MESSAGE)
        return cls.desktop

    @classmethod
    def getDocument(cls):
        """
        Returns current document component.
        RuntimeError is raised if setup() is not called before this.
        """
        return cls.getDesktop().getCurrentComponent()

    @classmethod
    def getServiceManager(cls):
        """
        Returns ServiceManager.
        """
        if not hasattr(cls, 'desktop'):
            raise RuntimeError(cls.EXCEPTION_MESSAGE)
        return cls.serviceManager

    @classmethod
    def getContext(cls):
        """
        Returns context.
        """
        if not hasattr(cls, 'desktop'):
            raise RuntimeError(cls.EXCEPTION_MESSAGE)
        return cls.context

    @classmethod
    def createInstance(cls, objectName):
        """
        Construct instance of given UNO object and return it. Return None if
        object is not found.
        """
        return cls.getDocument().createInstance(objectName)
