def filterRows(function, rows):
    """
    Filter rows with given filter function and return only rows that returns true.
    """
    return (y for y in rows if function(y))
