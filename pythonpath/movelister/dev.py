import pprint


def printMethods(obj):
    """
    Print given object methods. Check object's documentation for details.
    """
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(dir(obj))


def printAttributes(obj):
    """
    Print given object attributes. Check object's documentation for details.
    """
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(obj.__dict__)
