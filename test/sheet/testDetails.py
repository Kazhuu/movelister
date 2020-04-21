from test.officeTestCase import OfficeTestCase
from movelister.sheet.details import Details


class DetailsTestCase(OfficeTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.detailsName = 'Details (default)'
        cls.details = Details.fromSheet(cls.detailsName)

    def testDetailsInstance(self):
        self.assertTrue(self.details.data)
        self.assertEqual(self.details.modifiersColumnIndex, 1)
        self.assertEqual(self.details.inputToCompareColumnIndex, 2)
