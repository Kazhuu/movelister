import string
from movelister.core.context import Context


def convertIntoBaseAddress(num):
    """
    This code converts column number into base address (Base 26) since some LibreOffice features need it.
    """
    chars = []
    while num > 0:
        num, d = _divmodFunction(num)
        chars.append(string.ascii_uppercase[d - 1])
    return ''.join(reversed(chars))


def _divmodFunction(n):
    a, b = divmod(n, 26)
    if b == 0:
        return a - 1, b + 26
    return a, b
