from test.officeTestCase import OfficeTestCase
from movelister.process.updateStyles import UpdateStyles
from movelister.core import styles


class OverviewFactoryTestCase(OfficeTestCase):

    def setUp(self):
        super().setUp()
        styles.removeNonDefaultStyles()
        self.assertFalse(styles.getNonDefaultStyles())

    def testUpdateStyles(self):
        UpdateStyles.update()
        cellStyles = styles.getNonDefaultStyles()
        self.assertIn('(Action/Default)/Swim', cellStyles)
        self.assertIn('(Input/Default)/Move', cellStyles)
        self.assertIn('(Result)/No effect', cellStyles)
