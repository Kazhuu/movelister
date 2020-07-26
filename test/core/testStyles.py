from test.officeTestCase import OfficeTestCase
from movelister.core import styles
from movelister.model.color import Color
from com.sun.star.container import ElementExistException


class StylesTestCase(OfficeTestCase):

    def testGetStyles(self):
        cellStyles = styles.getCellStyles()
        self.assertIn('Default', cellStyles)
        self.assertIn('Heading 1', cellStyles)
        self.assertIn('Good', cellStyles)

    def testGetNonDefaultStyles(self):
        name = 'non default style'
        styles.addCellStyle(name, Color(-1))
        cellStyles = styles.getNonDefaultStyles()
        self.assertIn(name, cellStyles)

    def testRemoveNonDefaultStyles(self):
        styles.removeNonDefaultStyles()
        cellStyles = styles.getNonDefaultStyles()
        self.assertFalse(cellStyles)

    def testAddCellStyle(self):
        name = 'test style'
        color = Color(-1)
        styles.addCellStyle(name, color)
        cellStyle = styles.getCellStyleByName(name)
        self.assertEqual(cellStyle.getName(), name)
        self.assertEqual(cellStyle.CellBackColor, color.value)

    def testCreateTwoIdenticalStyles(self):
        name = 'test styles'
        styles.addCellStyle(name, Color(-1))
        with self.assertRaises(ElementExistException):
            styles.addCellStyle(name, Color(-1))
