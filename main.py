from movelister import environment


def kappa(*args):
    desktop = environment.getDesktop()
    model = desktop.getCurrentComponent()
    model.Sheets.insertNewByName("Nojes", 0)
    newSheet = model.Sheets.getByName("Nojes")
    newSheet.getCellByPosition(0, 0).setString("Test")
    a = 1
    testCell = newSheet.getCellByPosition(1, 1)
    testCell.setString(a)
    return None


# Tuple of exported functions seen by LibreOffice.
g_exportedScripts = (kappa,)

# Run when executed from the command line.
if __name__ == '__main__':
    kappa()
