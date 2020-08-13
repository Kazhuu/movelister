import os
import platform
import unittest
from subprocess import Popen

from movelister.core import file
from movelister.core.context import Context


class OfficeTestCase(unittest.TestCase):
    """
    TestCase class to handle LibreOffice file opening and reloading between
    tests. LibreOffice is opened in headless mode. Running tests also works
    when LibreOffice process is opened normally.

    Environment variables MV_LB_BIN is used to locate LibreOffice executable
    binary, defaults to 'soffice'. Environment variable MV_LB_PORT is used to
    provide port number for UNO socket connection, defaults to 8080.

    Certain tests which modify the sheet don't work on Windows, because the
    document is re-opened between tests in read-only mode. Tests work under
    Linux.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Get LibreOffice executable from env variable.
        libreOffice = os.environ.get('MV_LB_BIN', 'soffice')
        port = os.environ.get('MV_LB_PORT', 8080)
        # Open LibreOffice process differently if platform is Windows.
        system = platform.system()
        if system == 'Windows':
            cls.process = Popen(libreOffice + 'templates\movelister_test.ods \
                --norestore --accept=socket,host=127.0.0.1,port={0};urp'.format(port))
        else:
            cls.process = Popen(
                [libreOffice, 'templates/movelister_test.ods', '--headless', '--norestore',
                 '--accept=socket,host=127.0.0.1,port={0};urp'.format(port)])
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
