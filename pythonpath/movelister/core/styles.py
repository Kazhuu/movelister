import uno

from movelister.core.context import Context
from movelister.model.color import Color


def getCellStyleFamily():
    document = Context.getDocument()
    return document.getStyleFamilies().getByName('CellStyles')


def getCellStyles():
    return getCellStyleFamily().getElementNames()


def getCellStyleByName(name):
    return getCellStyleFamily().getByName(name)


def addCellStyle(name, color):
    if not isinstance(color, Color):
        raise TypeError('given color is not instance of Color')
    cellStyle = Context.createInstance('com.sun.star.style.CellStyle')
    getCellStyleFamily().insertByName(name, cellStyle)
    cellStyle.setPropertyValue('CellBackColor', color.value)


def getNonDefaultStyles():
    defaulStyles = ['Default', 'Accent', 'Accent 1', 'Accent 2', 'Accent 3',
        'Heading', 'Heading 1', 'Heading 2', 'Good', 'Bad', 'Neutral', 'Error',
        'Warning', 'Footnote', 'Note', 'Text', 'Hyperlink', 'Status'
    ]
    styles = getCellStyles()
    return [style for style in styles if style not in defaulStyles]

def removeNonDefaultStyles():
    styleFamily = getCellStyleFamily()
    cellStyles = getNonDefaultStyles()
    for cellStyle in cellStyles:
        styleFamily.removeByName(cellStyle)
