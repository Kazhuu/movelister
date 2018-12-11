def filterRows(function, rows):
    """
    Filter rows with given filter function and return only rows that returns
    true.
    """
    return [y for y in rows if function(y)]


def groupRows(rows, column):
    """
    Group rows from given column so that they contain the same column data.
    Consecutive data from given column is appended to same group. When data
    changes, new group is made. Cell with no data are excluded from groups.
    """
    filteredRows = filterRows(lambda row: row[column] != '', rows)
    groups = [[]]
    index = 0
    lastData = filteredRows[0][column]
    for row in filteredRows:
        if lastData != row[column]:
            index += 1
            lastData = row[column]
            groups.append([row])
        else:
            groups[index].append(row)
    return [group for group in groups]
