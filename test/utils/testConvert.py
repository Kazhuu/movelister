from test.officeTestCase import OfficeTestCase
from movelister.utils import convert


class ConvertTestCase(OfficeTestCase):

    def testConvertIntoBaseAddress(self):
        """
        Tests that the code to convert a number into Base 26 works like intended.
        """
        num1 = 26
        num2 = 27
        num3 = 702
        num4 = 703

        self.assertEqual(convert.convertIntoBaseAddress(num1), "Z")
        self.assertEqual(convert.convertIntoBaseAddress(num2), "AA")
        self.assertEqual(convert.convertIntoBaseAddress(num3), "ZZ")
        self.assertEqual(convert.convertIntoBaseAddress(num4), "AAA")
