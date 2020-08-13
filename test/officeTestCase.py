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

    Certain tests which modify the sheet don't work on Windows, because the
    document is re-opened between tests in read-only mode. Tests work under
    Linux.
    """
    BIN_EXCEPTION_MESSAGE = 'Set environment variable MV_LB_BIN to point to the LibreOffice executable before running tests.'
    PORT_ERROR_MESSAGE = 'Set environment variable MV_LB_PORT to given port number to use for UNO socket communication.'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Get LibreOffice executable from env variable.
        libreOffice = os.environ.get('MV_LB_BIN')
        port = os.environ.get('MV_LB_PORT')
        if libreOffice is None:
            raise RuntimeError(cls.BIN_EXCEPTION_MESSAGE)
        if port is None:
            raise RuntimeError(cls.PORT_ERROR_MESSAGE)
        # Open LibreOffice process differently if platform is Windows.
        system = platform.system()
        if system == 'Windows':
            cls.process = Popen(libreOffice + 'templates\movelister_test.ods \
                --norestore --accept=socket,host=127.0.0.1,port={0};urp'.format(port))
        else:
            cls.process = Popen(
                [libreOffice, 'templates/movelister_test.ods', '--headless', '--norestore',
                 '--accept=socket,host=127.0.0.1,port={0};urp'.format(port)])
        time.sleep(5)
        # Reset and setup context.
        Context.reset()
        Context.setup(host='127.0.0.1', port=port)

    @classmethod
    def tearDownClass(cls):
        # Terminate the opened process.
        cls.process.terminate()
        super().tearDownClass()

    def setUp(self):
        # Reopen the same file between each test case.
        file.reopenCurrentFile()
