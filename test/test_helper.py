import unittest
import time
from subprocess import Popen

from movelister.context import Context
from movelister import file


class OfficeTestCase(unittest.TestCase):
    """
    TestCase class to handle LibreOffice file opening and reloading
    between tests. LibreOffice is oppened in headless mode.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.process = Popen(
            ["libreoffice", "templates/movelister_template.ods", "--headless",
             "--accept=socket,host=localhost,port=2003;urp;StarOffice.ServiceManager"])
        time.sleep(1)
        Context.setup(host='localhost', port=2003)

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()
        super().tearDownClass()

    def setUp(self):
        file.reopenCurrentFile()
