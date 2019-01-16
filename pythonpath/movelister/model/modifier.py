class Modifier:

    def __init__(self, name, **kwargs):
        if not isinstance(name, str):
            raise ValueError('modifier must have a name as string')
        self.name = name
        self.color = kwargs.get('color', -1)

    def __eq__(self, other):
        """
        Test object equality.
        """
        return self.name == other.name

    def __ne__(self, other):
        """
        Test object nonequality.
        """
        return not self == other
