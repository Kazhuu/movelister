from test.officeTestCase import OfficeTestCase
from movelister.core.context import Context

class ContextTestCase(OfficeTestCase):

    def testSingletonServiceManager(self):
        """
        Test that returned service manager is a singleton object.
        """
        serviceManager1 = Context.getServiceManager()
        serviceManager2 = Context.getServiceManager()
        self.assertEqual(id(serviceManager1), id(serviceManager2))
