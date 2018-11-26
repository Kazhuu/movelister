from movelister import cursor


def setDataValidationToColumn(sheet, column, type):
    """
    This code sets a specific type of data validation to a single column.

    ValidationType ENUM = (0) ANY, (1) WHOLE, (2) DECIMAL, (3) DATE, (4) TIME, (5) TEXT_LEN, (6) LIST, (7) CUSTOM
    ValidationAlertStyle ENUM = (0) STOP, (1) WARNING, (2) INFO, (3) MACRO
    ConditionOperator ENUM = (0) NONE, (1) EQUAL, (2) NOT_EQUAL, (3) GREATER, (4) GREATER_EQUAL, (5) LESS
                             (6) LESS_EQUAL, (7) BETWEEN, (8) NOT_BETWEEN, (9) FORMULA
    """
    area = cursor.getUsedAreaSize(sheet)
    range = sheet.getCellRangeByPosition(column, 1, column, area.EndRow)
    validation = range.Validation

    if type == "phase":
        validation.Type = 2
        validation.ErrorAlertStyle = 0
        validation.setOperator(7)

        validation.ErrorMessage = "Please enter an integer between 0 and 99."
        validation.ShowErrorMessage = True

        validation.setFormula1(0.0)
        validation.setFormula2(99.0)

    if type == 'disable':
        validation.Type = 5
        validation.ErrorAlertStyle = 0
        validation.setOperator(1)

        validation.ErrorMessage = 'The content of this column are generated automatically. Don\'t modify it by hand.'
        validation.ShowErrorMessage = True

        validation.setFormula1(0.0)

    range.Validation = validation
