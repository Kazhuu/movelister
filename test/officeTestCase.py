import os
import platform
import time
import unittest
from subprocess import Popen

from movelister.core import file
from movelister.core.context import Context


class OfficeTestCase(unittest.TestCase):
    """
    TestCase class to handle LibreOffice file opening and reloading between
    tests. LibreOffice is opened in headless mode. Running tests also works
    when LibreOffice process is opened normally.

    TODO: certain tests which modify the sheet don't work on Windows, because
    the document is re-opened between tests in read-only mode. This seems to
    happen because of reopenCurrentFile function.
    """
    EXCEPTION_MESSAGE = 'Set environment variable MV_LB_BIN to point to the LibreOffice executable before running tests.'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Get LibreOffice executable from env variable.
        libreOffice = os.environ.get('MV_LB_BIN')
        if libreOffice is None:
            raise RuntimeError(cls.EXCEPTION_MESSAGE)
        # Open LibreOffice process differently if platform is Windows.
        system = platform.system()
        if system == 'Windows':
            cls.process = Popen(libreOffice + "templates\movelister_template.ods --headless \
                --accept=socket,host=localhost,port=2003;urp;StarOffice.ServiceManager")
        else:
            cls.process = Popen(
                [libreOffice, "templates/movelister_template.ods", "--headless",
                 "--accept=socket,host=localhost,port=2003;urp;StarOffice.ServiceManager"])
        time.sleep(1)
        # Reset and setup context.
        Context.reset()
        Context.setup(host='localhost', port=2003)

    @classmethod
    def tearDownClass(cls):
        # Terminate the opened process.
        cls.process.terminate()
        super().tearDownClass()

    def setUp(self):
        # Reopen the same file between each test case.
        file.reopenCurrentFile()
