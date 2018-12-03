import os
import platform
import time
import unittest
from subprocess import Popen

from movelister.context import Context
from movelister import file


class OfficeTestCase(unittest.TestCase):
    """
    TestCase class to handle LibreOffice file opening and reloading between
    tests. LibreOffice is oppened in headless mode. Running tests also work
    when LibreOffice process is oppened normally.
    """
    EXCEPTION_MESSAGE = 'set environment variable MV_LB_BIN to point to LibreOffice executable before running tests'

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
        # Between each test case, reopen the same file.
        file.reopenCurrentFile()
